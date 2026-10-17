from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ParkingPlaceType
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.parking_session import ParkingSession


class Rate(Base):
    name: Mapped[str] = mapped_column(String(150))
    price_per_hour: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    minimum_charge: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(default=True)
    place_type: Mapped[ParkingPlaceType] = mapped_column(
        Enum(ParkingPlaceType, name="parking_type_enum"),
        server_default=ParkingPlaceType.REGULAR.value,
    )

    parking_sessions: Mapped[list["ParkingSession"]] = relationship(
        back_populates="rate", lazy="raise"
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_rate_name"),
        CheckConstraint("price_per_hour > 0", name="ck_positive_price_per_hour"),
        CheckConstraint("minimum_charge >= 0", name="ck_non_negative_minimum_charge"),
    )
