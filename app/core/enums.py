from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class UserRole(StrEnum):
    USER = "USER"
    INSPECTOR = "INSPECTOR"
    ADMIN = "ADMIN"


class ParkingPlaceType(StrEnum):
    REGULAR = "REGULAR"
    DISABLED = "DISABLED"
    VIP = "VIP"


class ParkingPlaceStatus(StrEnum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    BLOCKED = "BLOCKED"


class ParkingSessionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    PAID = "PAID"


class FineStatus(StrEnum):
    PAID = "PAID"
    UNPAID = "UNPAID"
