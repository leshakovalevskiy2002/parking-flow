from sqlalchemy import select

from app.core.enums import ParkingPlaceStatus, ParkingPlaceType
from app.models.parking_place import ParkingPlace


class ParkingPlaceRepository:
    def __init__(self, session):
        self.session = session

    async def get_parking_places(self) -> list[ParkingPlace]:
        result = await self.session.scalars(select(ParkingPlace))
        return result.all()

    async def get_by_number(self, number: str) -> ParkingPlace:
        query = select(ParkingPlace).where(ParkingPlace.number == number)
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def find_first_free(self) -> ParkingPlace | None:
        query = (
            select(ParkingPlace)
            .where(ParkingPlace.status == ParkingPlaceStatus.FREE)
            .order_by(ParkingPlace.number)
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self, number: str, place_type: ParkingPlaceType, status: ParkingPlaceStatus
    ) -> ParkingPlace:
        place = ParkingPlace(number=number, type=place_type, status=status)
        self.session.add(place)
        await self.session.flush()
        return place

    async def delete(self, parking_place: ParkingPlace) -> None:
        await self.session.delete(parking_place)
        await self.session.flush()
        return
