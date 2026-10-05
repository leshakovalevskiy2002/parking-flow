from datetime import UTC, datetime, timedelta
from enum import StrEnum

import jwt
from pwdlib import PasswordHash

from app.config.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_token(data: dict, token_type: TokenType, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = (
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            if token_type == TokenType.ACCESS
            else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

    now = datetime.now(tz=UTC)
    to_encode.update({"exp": now + expires_delta, "iat": now, "type": token_type.value})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: TokenType) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("type") != expected_type.value:
        raise jwt.InvalidTokenError("Invalid token type")
    return payload
