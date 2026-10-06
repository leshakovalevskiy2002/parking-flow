from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.security import get_admin_user
from app.dependencies import get_parking_place_service, get_unit_of_work
from app.models import User
from app.schemas.parking_places import (
    ParkingPlaceRequest,
    ParkingPlaceResponse,
    UpdateParkingPlaceRequest,
)
from app.services.exceptions.parking_places import (
    ParkingPlaceAlreadyExistsError,
    ParkingPlaceIsOccupiedError,
    ParkingPlaceNotExistsError,
)
from app.services.parking_places_service import ParkingPlaceService
from app.uow import UnitOfWork

router = APIRouter(tags=["parking_places"], prefix="/parking_places")


@router.get("", response_model=list[ParkingPlaceResponse])
async def get_parking_places(
    _: Annotated[User, Depends(get_admin_user)],
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
):
    return await uow.parking_places.get_parking_places()


@router.post("", response_model=ParkingPlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_parking_place(
    parking_place_body: ParkingPlaceRequest,
    _: Annotated[User, Depends(get_admin_user)],
    parking_place_service: Annotated[ParkingPlaceService, Depends(get_parking_place_service)],
):
    try:
        return await parking_place_service.create_parking_place(
            number=parking_place_body.number,
            place_type=parking_place_body.type,
            status=parking_place_body.status,
        )
    except ParkingPlaceAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{place_number}", response_model=ParkingPlaceResponse)
async def get_parking_place_by_number(
    place_number: str,
    _: Annotated[User, Depends(get_admin_user)],
    parking_place_service: Annotated[ParkingPlaceService, Depends(get_parking_place_service)],
):
    try:
        return await parking_place_service.get_parking_place_by_number(place_number)
    except ParkingPlaceNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{place_number}", response_model=ParkingPlaceResponse)
async def update_parking_place(
    place_number: str,
    parking_place_body: UpdateParkingPlaceRequest,
    _: Annotated[User, Depends(get_admin_user)],
    parking_place_service: Annotated[ParkingPlaceService, Depends(get_parking_place_service)],
):
    try:
        return await parking_place_service.update_parking_place(
            number=place_number,
            new_number=parking_place_body.number,
            new_place_type=parking_place_body.type,
            new_status=parking_place_body.status,
        )
    except ParkingPlaceNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ParkingPlaceAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{place_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking_place(
    place_number: str,
    _: Annotated[User, Depends(get_admin_user)],
    parking_place_service: Annotated[ParkingPlaceService, Depends(get_parking_place_service)],
) -> None:
    try:
        return await parking_place_service.delete_parking_place(place_number)
    except ParkingPlaceNotExistsError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ParkingPlaceIsOccupiedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
