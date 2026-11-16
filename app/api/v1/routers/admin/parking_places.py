from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.v1.security import get_admin_user
from app.dependencies import ParkingPlaceServiceDep, get_unit_of_work
from app.schemas.parking_places import (
    ParkingPlaceRequest,
    ParkingPlaceResponse,
    UpdateParkingPlaceRequest,
)
from app.uow import UnitOfWork

router = APIRouter(
    tags=["parking_places"], prefix="/admin/parking_places", dependencies=[Depends(get_admin_user)]
)


@router.get("", response_model=list[ParkingPlaceResponse])
async def get_parking_places(uow: Annotated[UnitOfWork, Depends(get_unit_of_work)]):
    return await uow.parking_places.get_parking_places()


@router.post("", response_model=ParkingPlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_parking_place(
    parking_place_body: ParkingPlaceRequest,
    parking_place_service: ParkingPlaceServiceDep,
):
    return await parking_place_service.create_parking_place(
        number=parking_place_body.number,
        place_type=parking_place_body.type,
        status=parking_place_body.status,
    )


@router.get("/{place_number}", response_model=ParkingPlaceResponse)
async def get_parking_place_by_number(
    place_number: str,
    parking_place_service: ParkingPlaceServiceDep,
):
    return await parking_place_service.get_parking_place_by_number(place_number)


@router.patch("/{place_number}", response_model=ParkingPlaceResponse)
async def update_parking_place(
    place_number: str,
    parking_place_body: UpdateParkingPlaceRequest,
    parking_place_service: ParkingPlaceServiceDep,
):
    return await parking_place_service.update_parking_place(
        number=place_number,
        new_number=parking_place_body.number,
        new_place_type=parking_place_body.type,
        new_status=parking_place_body.status,
    )


@router.delete("/{place_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking_place(
    place_number: str,
    parking_place_service: ParkingPlaceServiceDep,
) -> None:
    return await parking_place_service.delete_parking_place(place_number)
