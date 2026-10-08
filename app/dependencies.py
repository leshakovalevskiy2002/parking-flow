from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from app.config.settings import async_session_maker
from app.services.auth_service import AuthService
from app.services.parking_places_service import ParkingPlaceService
from app.services.rates_service import RateService
from app.uow import UnitOfWork


async def get_unit_of_work() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(async_session_maker) as uow:
        yield uow


async def get_auth_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> AuthService:
    return AuthService(uow)


async def get_parking_place_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> ParkingPlaceService:
    return ParkingPlaceService(uow)


async def get_rate_service(uow: Annotated[UnitOfWork, Depends(get_unit_of_work)]) -> RateService:
    return RateService(uow)
