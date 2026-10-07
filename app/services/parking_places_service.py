from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.enums import ParkingPlaceStatus, ParkingPlaceType
from app.models import ParkingPlace
from app.services.exceptions.parking_places import (
    ParkingPlaceAlreadyExistsError,
    ParkingPlaceIsOccupiedError,
    ParkingPlaceNotExistsError,
)
from app.uow import UnitOfWork


class ParkingPlaceService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_parking_place(
        self, number: str, place_type: ParkingPlaceType, status: ParkingPlaceStatus
    ) -> ParkingPlace:
        existing = await self.uow.parking_places.get_by_number(number)

        if existing:
            raise ParkingPlaceAlreadyExistsError(number)

        try:
            return await self.uow.parking_places.create(number, place_type, status)
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__

            if isinstance(original_exception, UniqueViolationError):
                raise ParkingPlaceAlreadyExistsError(number) from exc
            raise

    async def get_parking_place_by_number(self, number: str) -> ParkingPlace:
        parking_place = await self.uow.parking_places.get_by_number(number.upper())

        if parking_place is None:
            raise ParkingPlaceNotExistsError(number)

        return parking_place

    async def update_parking_place(
        self,
        number: str,
        new_number: str | None,
        new_place_type: ParkingPlaceType | None,
        new_status: ParkingPlaceStatus | None,
    ) -> ParkingPlace:
        parking_place = await self.get_parking_place_by_number(number)

        if new_place_type is not None:
            parking_place.type = new_place_type

        if new_status is not None:
            parking_place.status = new_status

        if new_number is not None:
            parking_place.number = new_number

        try:
            await self.uow.flush()
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__
            if isinstance(original_exception, UniqueViolationError):
                raise ParkingPlaceAlreadyExistsError(parking_place.number) from exc
            raise

        return parking_place

    async def delete_parking_place(self, number: str) -> None:
        parking_place = await self.get_parking_place_by_number(number)

        if parking_place.status == ParkingPlaceStatus.OCCUPIED:
            raise ParkingPlaceIsOccupiedError(number)

        await self.uow.parking_places.delete(parking_place)
