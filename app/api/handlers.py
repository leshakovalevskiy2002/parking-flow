from fastapi import Request, status
from starlette.responses import JSONResponse

from app.domain.errors import (
    AuthError,
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    ParkingPlaceAlreadyExistsError,
    ParkingPlaceError,
    ParkingPlaceIsOccupiedError,
    ParkingPlaceNotExistsError,
    ParkingSessionError,
    RateAlreadyExistsError,
    RateError,
    RateInUseError,
    RateNotExistsError,
    TokenValidationError,
    UserError,
)


def _get_status_code_for_parking_place_error(exc: ParkingPlaceError) -> int:
    if isinstance(exc, ParkingPlaceAlreadyExistsError):
        return status.HTTP_400_BAD_REQUEST
    if isinstance(exc, ParkingPlaceNotExistsError):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, ParkingPlaceIsOccupiedError):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def _get_status_code_for_rate_error(exc: RateError) -> int:
    if isinstance(exc, RateAlreadyExistsError):
        return status.HTTP_400_BAD_REQUEST
    if isinstance(exc, RateNotExistsError):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, RateInUseError):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def _get_status_code_for_auth_error(exc: AuthError) -> int:
    if isinstance(exc, (ExpiredTokenError, InvalidCredentialsError, TokenValidationError)):
        return status.HTTP_401_UNAUTHORIZED
    if isinstance(exc, InactiveUserError):
        return status.HTTP_403_FORBIDDEN
    return status.HTTP_400_BAD_REQUEST


async def parking_place_exception_handler(
    _request: Request, exc: ParkingPlaceError
) -> JSONResponse:
    return JSONResponse(
        status_code=_get_status_code_for_parking_place_error(exc),
        content={"detail": str(exc)},
    )


async def rate_exception_handler(_request: Request, exc: RateError) -> JSONResponse:
    return JSONResponse(
        status_code=_get_status_code_for_rate_error(exc),
        content={"detail": str(exc)},
    )


async def user_exception_handler(_request: Request, exc: UserError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def parking_session_exception_handler(
    _request: Request, exc: ParkingSessionError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def auth_exception_handler(_request: Request, exc: AuthError) -> JSONResponse:
    headers = None
    if isinstance(exc, (ExpiredTokenError, InvalidCredentialsError, TokenValidationError)):
        headers = {"WWW-Authenticate": "Bearer"}

    return JSONResponse(
        status_code=_get_status_code_for_auth_error(exc),
        content={"detail": str(exc)},
        headers=headers,
    )
