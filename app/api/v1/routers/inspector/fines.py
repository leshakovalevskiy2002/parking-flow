from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.api.v1.security import get_inspector_user
from app.core.enums import FineStatus
from app.dependencies import get_fines_service
from app.domain.errors import ParkingError
from app.models import User
from app.schemas.fines import CreateFineRequest, FineListAdminResponse, FineResponse
from app.services.fines_service import FinesService

router = APIRouter(tags=["inspector", "fines"], prefix="/inspector/fines")


@router.post("", response_model=FineResponse, status_code=status.HTTP_201_CREATED)
async def create_fine(
    inspector: Annotated[User, Depends(get_inspector_user)],
    fines_service: Annotated[FinesService, Depends(get_fines_service)],
    fine_request_body: CreateFineRequest,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    try:
        return await fines_service.create_fine(
            inspector, fine_request_body.car_number, idempotency_key
        )
    except ParkingError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc


@router.get("", response_model=FineListAdminResponse)
async def get_fines(
    inspector: Annotated[User, Depends(get_inspector_user)],
    fines_service: Annotated[FinesService, Depends(get_fines_service)],
    car_number: str | None = Query(None, max_length=16),
    user_id: UUID | None = None,
    fine_status: FineStatus | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return await fines_service.get_fines(
        inspector_id=inspector.id,
        user_id=user_id,
        car_number=car_number,
        status=fine_status,
        from_date=from_date,
        to_date=to_date,
        page=page,
        size=size,
    )
