from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.v1.security import get_admin_user
from app.dependencies import RateServiceDep, get_unit_of_work
from app.schemas.rates import CreateRateRequest, RateResponse, UpdateRateRequest
from app.uow import UnitOfWork

router = APIRouter(tags=["rates"], prefix="/admin/rates", dependencies=[Depends(get_admin_user)])


@router.get("", response_model=list[RateResponse])
async def get_rates(uow: Annotated[UnitOfWork, Depends(get_unit_of_work)]):
    return await uow.rates.get_rates()


@router.post("", response_model=RateResponse, status_code=status.HTTP_201_CREATED)
async def create_rate(
    rate_body: CreateRateRequest,
    rate_service: RateServiceDep,
):
    return await rate_service.create_rate(
        name=rate_body.name,
        price_per_hour=rate_body.price_per_hour,
        minimum_charge=rate_body.minimum_charge,
        place_type=rate_body.place_type,
    )


@router.get("/{rate_name}", response_model=RateResponse)
async def get_rate_by_name(
    rate_name: str,
    rate_service: RateServiceDep,
):
    return await rate_service.get_rate_by_name(rate_name)


@router.patch("/{rate_name}", response_model=RateResponse)
async def update_rate(
    rate_name: str,
    rate_body: UpdateRateRequest,
    rate_service: RateServiceDep,
):
    return await rate_service.update_rate(
        name=rate_name,
        new_name=rate_body.name,
        new_price_per_hour=rate_body.price_per_hour,
        new_minimum_charge=rate_body.minimum_charge,
        new_place_type=rate_body.place_type,
    )


@router.delete("/{rate_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rate(
    rate_name: str,
    rate_service: RateServiceDep,
) -> None:
    return await rate_service.delete_rate(rate_name)
