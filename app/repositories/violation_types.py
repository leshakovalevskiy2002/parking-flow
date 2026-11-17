from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.violation_type import ViolationType


class ViolationTypeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_violation_types(self, include_inactive: bool = False) -> Sequence[ViolationType]:
        query = select(ViolationType).order_by(ViolationType.code)
        if not include_inactive:
            query = query.where(ViolationType.is_active.is_(True))
        result = await self.session.scalars(query)
        return result.all()

    async def get_by_id(self, violation_type_id: UUID) -> ViolationType | None:
        query = select(ViolationType).where(ViolationType.id == violation_type_id)
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def update(self, violation_type: ViolationType, **fields) -> ViolationType:
        for key, value in fields.items():
            setattr(violation_type, key, value)
        await self.session.flush()
        return violation_type
