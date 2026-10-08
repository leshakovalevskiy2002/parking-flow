from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.security import get_admin_user
from app.dependencies import get_rate_service, get_unit_of_work
from app.models import User
from app.schemas.rates import CreateRateRequest, RateResponse, UpdateRateRequest
from app.services.exceptions.rates import RateAlreadyExistsError, RateInUseError, RateNotExistsError
from app.services.rates_service import RateService
from app.uow import UnitOfWork

router = APIRouter(tags=["rates"], prefix="/rates")


@router.get("", response_model=list[RateResponse])
async def get_rates(
    _: Annotated[User, Depends(get_admin_user)],
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
):
    return await uow.rates.get_rates()


@router.post("", response_model=RateResponse, status_code=status.HTTP_201_CREATED)
async def create_rate(
    rate_body: CreateRateRequest,
    _: Annotated[User, Depends(get_admin_user)],
    rate_service: Annotated[RateService, Depends(get_rate_service)],
):
    try:
        return await rate_service.create_rate(
            name=rate_body.name,
            price_per_hour=rate_body.price_per_hour,
            minimum_charge=rate_body.minimum_charge,
        )
    except RateAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{rate_name}", response_model=RateResponse)
async def get_rate_by_name(
    rate_name: str,
    _: Annotated[User, Depends(get_admin_user)],
    rate_service: Annotated[RateService, Depends(get_rate_service)],
):
    try:
        return await rate_service.get_rate_by_name(rate_name)
    except RateNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{rate_name}", response_model=RateResponse)
async def update_rate(
    rate_name: str,
    rate_body: UpdateRateRequest,
    _: Annotated[User, Depends(get_admin_user)],
    rate_service: Annotated[RateService, Depends(get_rate_service)],
):
    try:
        return await rate_service.update_rate(
            name=rate_name,
            new_name=rate_body.name,
            new_price_per_hour=rate_body.price_per_hour,
            new_minimum_charge=rate_body.minimum_charge,
        )
    except RateNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RateAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{rate_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rate(
    rate_name: str,
    _: Annotated[User, Depends(get_admin_user)],
    rate_service: Annotated[RateService, Depends(get_rate_service)],
) -> None:
    try:
        return await rate_service.delete_rate(rate_name)
    except RateNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RateInUseError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
