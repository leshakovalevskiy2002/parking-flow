from datetime import UTC, datetime
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.enums import ParkingPlaceStatus, ParkingSessionStatus
from app.domain.errors import CarAlreadyParkedError, CarNotParkedError, NoFreePlaceError
from app.domain.pricing import calculate_cost
from app.models import ParkingSession, User
from app.services.exceptions.rates import RateNotExistsError
from app.uow import UnitOfWork


class ParkingSessionsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def check_in(self, user: User, car_number: str, rate_name: str) -> ParkingSession:
        rate = await self.uow.rates.get_by_name(rate_name)

        if rate is None:
            raise RateNotExistsError(rate_name)

        active_session = await self.uow.parking_sessions.get_active_session_by_car_number(
            car_number
        )
        if active_session:
            raise CarAlreadyParkedError(car_number)

        free_place = await self.uow.parking_places.find_first_free()
        if free_place is None:
            raise NoFreePlaceError()

        free_place.status = ParkingPlaceStatus.OCCUPIED

        try:
            parking_session = await self.uow.parking_sessions.create(
                user_id=user.id,
                place_id=free_place.id,
                rate_id=rate.id,
                car_number=car_number,
                hourly_rate_snapshot=rate.price_per_hour,
                minimum_charge_snapshot=rate.minimum_charge,
            )
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__

            if isinstance(original_exception, UniqueViolationError):
                constraint_name = getattr(original_exception, "constraint_name", None)

                if constraint_name == "uq_active_session_per_car":
                    raise CarAlreadyParkedError(car_number) from exc
                if constraint_name == "uq_active_session_per_place":
                    raise NoFreePlaceError() from exc
            raise

        return parking_session

    async def check_out(self, car_number: str):
        active_session = await self.uow.parking_sessions.get_active_session_by_car_number(
            car_number
        )

        if not active_session:
            raise CarNotParkedError(car_number)

        start_time = active_session.start_time
        end_time = datetime.now(tz=UTC)
        price_per_hour = active_session.hourly_rate_snapshot
        minimum_charge = active_session.minimum_charge_snapshot

        total_cost = calculate_cost(start_time, end_time, price_per_hour, minimum_charge)

        closed = await self.uow.parking_sessions.close_if_active(
            session_id=active_session.id, end_time=end_time, total_cost=total_cost
        )
        if not closed:
            raise CarNotParkedError(car_number)

        await self.uow.parking_places.refresh_status(active_session.place_id)

        return {
            "session_id": active_session.id,
            "start_time": start_time,
            "end_time": end_time,
            "total_cost": total_cost,
        }

    async def get_parking_sessions(
        self,
        user_id: UUID | None,
        status: ParkingSessionStatus | None,
        car_number: str | None,
        place_id: UUID | None = None,
        rate_id: UUID | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        page: int = 1,
        size: int = 10,
    ):
        filters = []
        if user_id is not None:
            filters.append(ParkingSession.user_id == user_id)
        if status is not None:
            filters.append(ParkingSession.status == status)
        if car_number is not None:
            filters.append(ParkingSession.car_number == car_number.upper())
        if place_id is not None:
            filters.append(ParkingSession.place_id == place_id)
        if rate_id is not None:
            filters.append(ParkingSession.rate_id == rate_id)
        if from_date is not None:
            filters.append(ParkingSession.start_time >= from_date)
        if to_date is not None:
            filters.append(ParkingSession.start_time <= to_date)

        items, total = await self.uow.parking_sessions.get_paginated(
            filters=filters,
            page=page,
            size=size,
            order_by=ParkingSession.car_number.asc(),
        )

        return {"items": items, "total": total, "page": page, "size": size}
