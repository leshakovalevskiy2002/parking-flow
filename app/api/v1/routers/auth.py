from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_auth_service
from app.schemas.auth import RefreshRequest, TokenPair
from app.schemas.users import UserRegisterRequest, UserResponse
from app.services.auth_service import AuthService
from app.services.exceptions.auth import (
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    TokenValidationError,
)
from app.services.exceptions.users import UserAlreadyExistsError

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserRegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.register(user_data.email, user_data.password.get_secret_value())
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/token", response_model=TokenPair)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(email=form_data.username, password=form_data.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except InactiveUserError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    body: RefreshRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.refresh(refresh_token=body.refresh_token)
    except (TokenValidationError, ExpiredTokenError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except InactiveUserError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
