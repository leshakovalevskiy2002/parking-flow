from uuid import UUID

from app.domain.errors import ViolationTypeNotFoundError
from app.uow import UnitOfWork


class ViolationTypeService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_violation_type_by_id(self, violation_type_id: UUID):
        violation_type = await self.uow.violation_types.get_by_id(violation_type_id)
        if violation_type is None:
            raise ViolationTypeNotFoundError(str(violation_type_id))
        return violation_type

    async def update_violation_type(self, violation_type_id: UUID, fields: dict):
        violation_type = await self.get_violation_type_by_id(violation_type_id)
        if not fields:
            return violation_type
        return await self.uow.violation_types.update(violation_type, **fields)

    async def deactivate(self, violation_type_id: UUID):
        violation_type = await self.get_violation_type_by_id(violation_type_id)
        return await self.uow.violation_types.update(violation_type, is_active=False)

    async def activate(self, violation_type_id: UUID):
        violation_type = await self.get_violation_type_by_id(violation_type_id)
        return await self.uow.violation_types.update(violation_type, is_active=True)
