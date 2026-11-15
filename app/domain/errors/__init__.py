from app.domain.errors.auth import (
    AuthError,
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    TokenValidationError,
)
from app.domain.errors.base import DomainError
from app.domain.errors.parking_place import (
    ParkingPlaceAlreadyExistsError,
    ParkingPlaceError,
    ParkingPlaceIsOccupiedError,
    ParkingPlaceNotExistsError,
)
from app.domain.errors.parking_session import (
    CarAlreadyParkedError,
    CarIsParkedLegallyError,
    CarNotParkedError,
    NoFreePlaceError,
    ParkingSessionError,
)
from app.domain.errors.rate import (
    RateAlreadyExistsError,
    RateError,
    RateInUseError,
    RateNotExistsError,
)
from app.domain.errors.user import UserAlreadyExistsError, UserError

__all__ = [
    "AuthError",
    "CarAlreadyParkedError",
    "CarIsParkedLegallyError",
    "CarNotParkedError",
    "DomainError",
    "ExpiredTokenError",
    "InactiveUserError",
    "InvalidCredentialsError",
    "NoFreePlaceError",
    "ParkingPlaceAlreadyExistsError",
    "ParkingPlaceError",
    "ParkingPlaceIsOccupiedError",
    "ParkingPlaceNotExistsError",
    "ParkingSessionError",
    "RateAlreadyExistsError",
    "RateError",
    "RateInUseError",
    "RateNotExistsError",
    "TokenValidationError",
    "UserAlreadyExistsError",
    "UserError",
]
