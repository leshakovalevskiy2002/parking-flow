from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.api.v1.security import get_inspector_user
from app.dependencies import get_fines_service
from app.domain.errors import ParkingError
from app.models import User
from app.schemas.fines import CreateFineRequest, FineResponse
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
