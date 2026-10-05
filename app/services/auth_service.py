from asyncpg import UniqueViolationError
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.core.enums import UserStatus
from app.core.security import (
    DUMMY_HASH,
    TokenType,
    create_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import TokenData, TokenPair
from app.services.exceptions.auth import (
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    TokenValidationError,
)
from app.services.exceptions.users import UserAlreadyExistsError
from app.uow import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @staticmethod
    def _access_payload(user: User) -> dict:
        return {"sub": str(user.id), "role": user.role.value}

    @staticmethod
    def _refresh_payload(user: User) -> dict:
        return {"sub": str(user.id)}

    async def _issue_token_pair(self, user: User) -> TokenPair:
        access_token = create_token(data=self._access_payload(user), token_type=TokenType.ACCESS)
        refresh_token = create_token(data=self._refresh_payload(user), token_type=TokenType.REFRESH)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def register(self, email: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        user = await self.uow.users.get_by_email(email)

        if user:
            raise UserAlreadyExistsError(email)

        try:
            return await self.uow.users.create_user(email, hashed_password)
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__

            if isinstance(original_exception, UniqueViolationError):
                raise UserAlreadyExistsError(email) from exc
            raise

    async def login(self, email: str, password: str) -> TokenPair:
        user = await self.uow.users.get_by_email(email)

        if not user:
            verify_password(password, DUMMY_HASH)
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        if user.status != UserStatus.ACTIVE:
            raise InactiveUserError()

        return await self._issue_token_pair(user)

    async def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
        except ExpiredSignatureError as exc:
            raise ExpiredTokenError() from exc
        except InvalidTokenError as exc:
            raise TokenValidationError() from exc

        try:
            token_data = TokenData(user_id=payload.get("sub"))
        except ValidationError as exc:
            raise TokenValidationError() from exc

        user = await self.uow.users.get_by_id(token_data.user_id)
        if user is None:
            raise TokenValidationError()

        if user.status != UserStatus.ACTIVE:
            raise InactiveUserError()

        return await self._issue_token_pair(user)
