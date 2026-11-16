from fastapi import FastAPI

from app.api.handlers import (
    auth_exception_handler,
    parking_place_exception_handler,
    parking_session_exception_handler,
    rate_exception_handler,
    user_exception_handler,
)
from app.domain.errors import (
    AuthError,
    ParkingPlaceError,
    ParkingSessionError,
    RateError,
    UserError,
)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ParkingPlaceError, parking_place_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RateError, rate_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(UserError, user_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ParkingSessionError, parking_session_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(AuthError, auth_exception_handler)  # type: ignore[arg-type]
