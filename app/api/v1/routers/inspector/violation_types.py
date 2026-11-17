from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.security import get_inspector_user
from app.dependencies import get_unit_of_work
from app.schemas.violation_types import ViolationTypeResponse
from app.uow import UnitOfWork

router = APIRouter(
    tags=["inspector", "violation_types"],
    prefix="/inspector/violation_types",
    dependencies=[Depends(get_inspector_user)],
)


@router.get("", response_model=list[ViolationTypeResponse])
async def get_active_violation_types(uow: Annotated[UnitOfWork, Depends(get_unit_of_work)]):
    return await uow.violation_types.get_violation_types(include_inactive=False)
