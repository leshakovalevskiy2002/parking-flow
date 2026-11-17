from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ViolationTypeResponse(BaseModel):
    id: UUID
    code: str
    reason: str
    amount: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateViolationTypeRequest(BaseModel):
    reason: Annotated[str, Field(min_length=1)] | None = None
    amount: Annotated[Decimal, Field(gt=0)] | None = None

    model_config = ConfigDict(extra="forbid")
