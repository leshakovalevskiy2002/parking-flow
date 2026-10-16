from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import FineStatus


class FineResponse(BaseModel):
    car_number: str
    user_id: UUID | None
    reason: str
    amount: Decimal
    issued_at: datetime


class CreateFineRequest(BaseModel):
    car_number: Annotated[str, Field(max_length=16)]

    @field_validator("car_number", mode="before")
    @classmethod
    def normalize(cls, car_number: str) -> str:
        if isinstance(car_number, str):
            return car_number.upper()
        return car_number


class FineItemResponse(BaseModel):
    id: UUID
    car_number: str
    reason: str
    amount: Decimal
    status: FineStatus
    issued_by_id: UUID
    issued_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FineListResponse(BaseModel):
    items: list[FineItemResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)


class FineItemAdminResponse(FineItemResponse):
    user_id: UUID | None


class FineListAdminResponse(BaseModel):
    items: list[FineItemAdminResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)
