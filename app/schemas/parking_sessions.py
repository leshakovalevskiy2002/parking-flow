from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import ParkingSessionStatus
from app.schemas.users import UserNestedResponse


class ParkingSessionBaseRequest(BaseModel):
    car_number: Annotated[str, Field(max_length=16)]

    @field_validator("car_number", mode="before")
    @classmethod
    def normalize_car_number(cls, car_number: str) -> str:
        if isinstance(car_number, str):
            return car_number.upper()
        return car_number


class ParkingSessionCheckInRequest(ParkingSessionBaseRequest):
    rate_name: Annotated[str, Field(max_length=150)]

    @field_validator("rate_name", mode="before")
    @classmethod
    def normalize_rate_name(cls, rate_name: str) -> str:
        if isinstance(rate_name, str):
            return rate_name.capitalize()
        return rate_name


class ParkingSessionCheckOutRequest(ParkingSessionBaseRequest):
    pass


class ParkingSessionCheckInResponse(BaseModel):
    id: UUID
    user_id: UUID
    place_id: UUID
    car_number: str
    start_time: datetime
    end_time: datetime | None
    status: ParkingSessionStatus
    hourly_rate_snapshot: Annotated[Decimal, Field(alias="hourly_rate")]
    minimum_charge_snapshot: Annotated[Decimal, Field(alias="minimum_charge")]

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)


class ParkingSessionCheckOutResponse(BaseModel):
    session_id: UUID
    start_time: datetime
    end_time: datetime
    total_cost: Decimal


class ParkingSessionItemResponse(BaseModel):
    id: UUID
    car_number: str
    status: ParkingSessionStatus
    start_time: datetime
    end_time: datetime | None
    total_cost: Decimal | None
    place_number: str
    rate_name: str

    model_config = ConfigDict(from_attributes=True)


class ParkingSessionListResponse(BaseModel):
    items: list[ParkingSessionItemResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)


class ParkingSessionItemAdminResponse(ParkingSessionItemResponse):
    user: UserNestedResponse
    hourly_rate_snapshot: Decimal
    minimum_charge_snapshot: Decimal


class ParkingSessionListAdminResponse(BaseModel):
    items: list[ParkingSessionItemAdminResponse]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)
