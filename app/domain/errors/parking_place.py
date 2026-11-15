from app.domain.errors.base import DomainError


class ParkingPlaceError(DomainError):
    """Parking place flow error"""


class ParkingPlaceAlreadyExistsError(ParkingPlaceError):
    code = "PARKING_PLACE_ALREADY_EXISTS"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` already exists")


class ParkingPlaceNotExistsError(ParkingPlaceError):
    code = "PARKING_PLACE_NOT_EXISTS"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` does not exist")


class ParkingPlaceIsOccupiedError(ParkingPlaceError):
    code = "PARKING_PLACE_IS_OCCUPIED"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` is occupied")
