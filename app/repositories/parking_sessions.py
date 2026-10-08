from decimal import Decimal
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

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
