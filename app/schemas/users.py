from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

from app.core.enums import UserStatus


class UserRegisterRequest(BaseModel):
    email: Annotated[EmailStr, Field(max_length=100)]
    password: Annotated[SecretStr, Field(min_length=8, max_length=64)]

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        if isinstance(email, str):
            return email.strip().lower()
        return email


class UserResponse(BaseModel):
    id: UUID
    email: str
    status: UserStatus
    created: datetime
    updated: datetime

    model_config = ConfigDict(from_attributes=True)
