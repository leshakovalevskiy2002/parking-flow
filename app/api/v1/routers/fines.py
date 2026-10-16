from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v1.security import get_current_active_user
from app.core.enums import FineStatus
from app.dependencies import get_fines_service
from app.models import User
from app.schemas.fines import FineListResponse
from app.services.fines_service import FinesService

router = APIRouter(tags=["fines"], prefix="/fines")


@router.get("", response_model=FineListResponse)
async def get_fines(
    current_user: Annotated[User, Depends(get_current_active_user)],
    fines_service: Annotated[FinesService, Depends(get_fines_service)],
    car_number: str | None = Query(None, max_length=16),
    status: FineStatus | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return await fines_service.get_fines(
        user_id=current_user.id,
        car_number=car_number,
        status=status,
        from_date=from_date,
        to_date=to_date,
        page=page,
        size=size,
    )
