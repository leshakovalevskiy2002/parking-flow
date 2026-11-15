from app.domain.errors import DomainError


class ParkingSessionError(DomainError):
    """Parking session flow error"""


class CarAlreadyParkedError(ParkingSessionError):
    code = "CAR_ALREADY_PARKED"

    def __init__(self, car_number: str) -> None:
        self.car_number = car_number
        super().__init__(f"Car with car_number `{car_number}` already parked")


class CarNotParkedError(ParkingSessionError):
    code = "CAR_NOT_PARKED"

    def __init__(self, car_number: str) -> None:
        self.car_number = car_number
        super().__init__(f"Car with car_number `{car_number}` not parked")


class NoFreePlaceError(ParkingSessionError):
    code = "NO_FREE_PLACE"

    def __init__(self) -> None:
        super().__init__("No free parking places")


class CarIsParkedLegallyError(ParkingSessionError):
    code = "CAR_IS_PARKED_LEGALLY"

    def __init__(self, car_number: str) -> None:
        self.car_number = car_number
        super().__init__(f"Car with car_number `{car_number}` parked legally")
