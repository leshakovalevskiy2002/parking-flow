from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CheckInRequest(BaseModel):
    car_number: Annotated[str, Field(max_length=16)]
    rate_name: Annotated[str, Field(max_length=150)]

    @field_validator("car_number", mode="before")
    @classmethod
    def normalize_car_number(cls, car_number: str) -> str:
        if isinstance(car_number, str):
            return car_number.upper()
        return car_number

    @field_validator("rate_name", mode="before")
    @classmethod
    def normalize_rate_name(cls, rate_name: str) -> str:
        if isinstance(rate_name, str):
            return rate_name.capitalize()
        return rate_name


class ParkingSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    place_id: UUID
    rate_id: UUID
    car_number: str
    start_time: datetime
    end_time: datetime | None
