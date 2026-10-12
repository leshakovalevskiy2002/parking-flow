from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.security import get_current_active_user
from app.core.enums import ParkingSessionStatus
from app.dependencies import get_parking_sessions_service
from app.domain.errors import ParkingError
from app.models import User
from app.schemas.parking_sessions import (
    ParkingSessionCheckInRequest,
    ParkingSessionCheckInResponse,
    ParkingSessionCheckOutRequest,
    ParkingSessionCheckOutResponse,
    ParkingSessionListResponse,
)
from app.services.exceptions.rates import RateNotExistsError
from app.services.parking_sessions_service import ParkingSessionsService

router = APIRouter(tags=["parking_sessions"], prefix="/parking_sessions")


@router.post("/check-in", response_model=ParkingSessionCheckInResponse)
async def check_in(
    check_in_body: ParkingSessionCheckInRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    parking_sessions_service: Annotated[
        ParkingSessionsService, Depends(get_parking_sessions_service)
    ],
):
    try:
        return await parking_sessions_service.check_in(
            user=user, car_number=check_in_body.car_number, rate_name=check_in_body.rate_name
        )
    except RateNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ParkingError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/check-out", response_model=ParkingSessionCheckOutResponse)
async def check_out(
    check_out_body: ParkingSessionCheckOutRequest,
    _: Annotated[User, Depends(get_current_active_user)],
    parking_sessions_service: Annotated[
        ParkingSessionsService, Depends(get_parking_sessions_service)
    ],
):
    try:
        return await parking_sessions_service.check_out(check_out_body.car_number)
    except ParkingError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=ParkingSessionListResponse)
async def get_parking_sessions(
    current_user: Annotated[User, Depends(get_current_active_user)],
    parking_sessions_service: Annotated[
        ParkingSessionsService, Depends(get_parking_sessions_service)
    ],
    session_status: ParkingSessionStatus | None = None,
    car_number: str | None = Query(None, max_length=16),
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return await parking_sessions_service.get_parking_sessions(
        user_id=current_user.id,
        status=session_status,
        car_number=car_number,
        from_date=from_date,
        to_date=to_date,
        page=page,
        size=size,
    )
