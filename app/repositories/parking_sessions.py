from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import exists, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import ColumnElement, UnaryExpression

from app.core.enums import ParkingSessionStatus
from app.models import ParkingSession


class ParkingSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists_by_rate_id(self, rate_id: UUID) -> bool:
        query = select(
            exists().where(
                ParkingSession.rate_id == rate_id,
                ParkingSession.status == ParkingSessionStatus.ACTIVE,
            )
        )
        return bool(await self.session.scalar(query))

    async def get_active_session_by_car_number(self, car_number: str) -> ParkingSession | None:
        query = select(ParkingSession).where(
            ParkingSession.car_number == car_number,
            ParkingSession.status == ParkingSessionStatus.ACTIVE,
        )
        return await self.session.scalar(query)

    async def create(
        self,
        user_id: UUID,
        place_id: UUID,
        rate_id: UUID,
        car_number: str,
        hourly_rate_snapshot: Decimal,
        minimum_charge_snapshot: Decimal,
    ) -> ParkingSession:
        parking_session = ParkingSession(
            user_id=user_id,
            place_id=place_id,
            rate_id=rate_id,
            car_number=car_number,
            hourly_rate_snapshot=hourly_rate_snapshot,
            minimum_charge_snapshot=minimum_charge_snapshot,
        )
        self.session.add(parking_session)
        await self.session.flush()
        return parking_session

    async def close_if_active(self, session_id: UUID, end_time: datetime, total_cost: Decimal):
        query = (
            update(ParkingSession)
            .where(
                ParkingSession.id == session_id,
                ParkingSession.status == ParkingSessionStatus.ACTIVE,
            )
            .values(end_time=end_time, total_cost=total_cost, status=ParkingSessionStatus.FINISHED)
        )
        result = await self.session.execute(query)
        return result.rowcount == 1  # type: ignore

    async def get_paginated(
        self,
        filters: list[ColumnElement[bool]],
        page: int,
        size: int,
        order_by: UnaryExpression,
    ) -> tuple[list[ParkingSession], int]:
        base_query = select(ParkingSession)
        if filters:
            base_query = base_query.where(*filters)

        count_query = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()

        items_query = (
            base_query.options(
                selectinload(ParkingSession.parking_place),
                selectinload(ParkingSession.rate),
                selectinload(ParkingSession.user),
            )
            .order_by(order_by)
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.session.scalars(items_query)
        items = list(result.all())

        return items, total
