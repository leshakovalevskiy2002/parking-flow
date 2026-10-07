class ParkingPlaceServiceError(Exception):
    pass


class ParkingPlaceAlreadyExistsError(ParkingPlaceServiceError):
    code = "PARKING_PLACE_ALREADY_EXISTS"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` already exists")


class ParkingPlaceNotExistsError(ParkingPlaceServiceError):
    code = "PARKING_PLACE_NOT_EXISTS"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` does not exist")


class ParkingPlaceIsOccupiedError(ParkingPlaceServiceError):
    code = "PARKING_PLACE_IS_OCCUPIED"

    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Parking place with number `{number}` is occupied")
