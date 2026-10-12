from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.v1.security import get_admin_user
from app.core.enums import ParkingSessionStatus
from app.dependencies import get_parking_sessions_service
from app.schemas.parking_sessions import ParkingSessionListAdminResponse
from app.services.parking_sessions_service import ParkingSessionsService

router = APIRouter(
    tags=["admin", "parking_sessions"],
    prefix="/admin/parking_sessions",
    dependencies=[Depends(get_admin_user)],
)


@router.get("", response_model=ParkingSessionListAdminResponse)
async def get_parking_sessions(
    parking_sessions_service: Annotated[
        ParkingSessionsService, Depends(get_parking_sessions_service)
    ],
    user_id: UUID | None = None,
    session_status: ParkingSessionStatus | None = None,
    car_number: str | None = Query(None, max_length=16),
    place_id: UUID | None = None,
    rate_id: UUID | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return await parking_sessions_service.get_parking_sessions(
        user_id=user_id,
        status=session_status,
        car_number=car_number,
        place_id=place_id,
        rate_id=rate_id,
        from_date=from_date,
        to_date=to_date,
        page=page,
        size=size,
    )
