from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


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
