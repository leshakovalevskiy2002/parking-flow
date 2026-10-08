from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.enums import ParkingPlaceStatus
from app.domain.errors import CarAlreadyParkedError, NoFreePlaceError
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
