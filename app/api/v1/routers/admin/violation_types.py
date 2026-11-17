from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.v1.security import get_admin_user
from app.dependencies import ViolationTypeServiceDep, get_unit_of_work
from app.schemas.violation_types import UpdateViolationTypeRequest, ViolationTypeResponse
from app.uow import UnitOfWork

router = APIRouter(
    tags=["violation_types"],
    prefix="/admin/violation_types",
    dependencies=[Depends(get_admin_user)],
)


@router.get("", response_model=list[ViolationTypeResponse])
async def get_violation_types(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    include_inactive: bool = False,
):
    return await uow.violation_types.get_violation_types(include_inactive=include_inactive)


@router.get("/{violation_type_id}", response_model=ViolationTypeResponse)
async def get_violation_type_by_id(
    violation_type_id: UUID,
    violation_service: ViolationTypeServiceDep,
):
    return await violation_service.get_violation_type_by_id(violation_type_id)


@router.patch("/{violation_type_id}", response_model=ViolationTypeResponse)
async def update_violation_type(
    violation_type_id: UUID,
    violation_type_body: UpdateViolationTypeRequest,
    violation_service: ViolationTypeServiceDep,
):
    return await violation_service.update_violation_type(
        violation_type_id,
        violation_type_body.model_dump(exclude_unset=True),
    )


@router.post("/{violation_type_id}/deactivate", response_model=ViolationTypeResponse)
async def deactivate_violation_type(
    violation_type_id: UUID,
    violation_service: ViolationTypeServiceDep,
):
    return await violation_service.deactivate(violation_type_id)


@router.post("/{violation_type_id}/activate", response_model=ViolationTypeResponse)
async def activate_violation_type(
    violation_type_id: UUID,
    violation_service: ViolationTypeServiceDep,
):
    return await violation_service.activate(violation_type_id)
