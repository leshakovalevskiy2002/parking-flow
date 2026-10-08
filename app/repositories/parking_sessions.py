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
