from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import ParkingPlaceStatus, ParkingPlaceType


class ParkingPlaceResponse(BaseModel):
    id: UUID
    number: str
    type: ParkingPlaceType
    status: ParkingPlaceStatus
    created: datetime
    updated: datetime

    model_config = ConfigDict(from_attributes=True)


class ParkingPlaceNumberValidationMixin:
    @field_validator("number", mode="before")
    @classmethod
    def normalize_number(cls, number: str | None) -> str | None:
        if isinstance(number, str):
            return number.upper()
        return number


class ParkingPlaceRequest(ParkingPlaceNumberValidationMixin, BaseModel):
    number: Annotated[str, Field(max_length=12)]
    type: ParkingPlaceType = ParkingPlaceType.REGULAR
    status: ParkingPlaceStatus = ParkingPlaceStatus.FREE


class UpdateParkingPlaceRequest(ParkingPlaceNumberValidationMixin, BaseModel):
    number: Annotated[str, Field(max_length=12)] | None = None
    type: ParkingPlaceType | None = None
    status: ParkingPlaceStatus | None = None
