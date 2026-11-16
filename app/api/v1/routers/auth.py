from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import AuthServiceDep
from app.schemas.auth import RefreshRequest, TokenPair
from app.schemas.users import UserRegisterRequest, UserResponse

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserRegisterRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.register(user_data.email, user_data.password.get_secret_value())


@router.post("/token", response_model=TokenPair)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    return await auth_service.login(email=form_data.username, password=form_data.password)


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    body: RefreshRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.refresh(refresh_token=body.refresh_token)
