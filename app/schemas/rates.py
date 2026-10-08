from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class RateResponse(BaseModel):
    id: UUID
    name: str
    price_per_hour: Decimal
    minimum_charge: Decimal
    created: datetime
    updated: datetime


class RateNameValidationMixin:
    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, name: str | None) -> str | None:
        if isinstance(name, str):
            return name.capitalize()
        return name


class CreateRateRequest(RateNameValidationMixin, BaseModel):
    name: Annotated[str, Field(max_length=150)]
    price_per_hour: Annotated[Decimal, Field(gt=Decimal("0.00"))]
    minimum_charge: Annotated[Decimal, Field(ge=Decimal("0.00"))]


class UpdateRateRequest(RateNameValidationMixin, BaseModel):
    name: Annotated[str, Field(max_length=150)] | None = None
    price_per_hour: Annotated[Decimal, Field(gt=Decimal("0.00"))] | None = None
    minimum_charge: Annotated[Decimal, Field(ge=Decimal("0.00"))] | None = None
