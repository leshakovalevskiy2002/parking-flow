from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from app.config.settings import async_session_maker
from app.services.auth_service import AuthService
from app.services.fines_service import FinesService
from app.services.parking_places_service import ParkingPlaceService
from app.services.parking_sessions_service import ParkingSessionsService
from app.services.rates_service import RateService
from app.services.violation_types_service import ViolationTypeService
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


async def get_parking_sessions_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> ParkingSessionsService:
    return ParkingSessionsService(uow)


async def get_fines_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> FinesService:
    return FinesService(uow)


async def get_violation_types_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> ViolationTypeService:
    return ViolationTypeService(uow)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
FinesServiceDep = Annotated[FinesService, Depends(get_fines_service)]
ParkingPlaceServiceDep = Annotated[ParkingPlaceService, Depends(get_parking_place_service)]
ParkingSessionsServiceDep = Annotated[ParkingSessionsService, Depends(get_parking_sessions_service)]
RateServiceDep = Annotated[RateService, Depends(get_rate_service)]
ViolationTypeServiceDep = Annotated[ViolationTypeService, Depends(get_violation_types_service)]
