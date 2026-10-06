from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError

from app.core.enums import UserRole, UserStatus
from app.core.security import TokenType, decode_token
from app.dependencies import get_unit_of_work
from app.models.user import User
from app.schemas.auth import TokenData
from app.uow import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> User:
    try:
        payload = decode_token(token, TokenType.ACCESS)
    except InvalidTokenError as exc:
        raise credentials_exception from exc

    try:
        token_data = TokenData(user_id=payload.get("sub"))
    except ValidationError as exc:
        raise credentials_exception from exc

    user = await uow.users.get_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_inspector_user(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if current_active_user.role != UserRole.INSPECTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not an inspector"
        )
    return current_active_user


async def get_admin_user(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if current_active_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")
    return current_active_user
