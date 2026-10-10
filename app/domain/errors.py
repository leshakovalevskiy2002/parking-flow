class DomainError(Exception):
    """Base domain exception"""

    code: str


class ParkingError(DomainError):
    """Parking flow error"""


class CarAlreadyParkedError(ParkingError):
    code = "CAR_ALREADY_PARKED"

    def __init__(self, car_number: str) -> None:
        self.car_number = car_number
        super().__init__(f"Car with car_number `{car_number}` already parked")


class NoFreePlaceError(ParkingError):
    code = "NO_FREE_PLACE"

    def __init__(self) -> None:
        super().__init__("No free parking places")
