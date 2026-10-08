from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.parking_session import ParkingSession


class Rate(Base):
    name: Mapped[str] = mapped_column(String(150))
    price_per_hour: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    minimum_charge: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(default=True)

    parking_sessions: Mapped[list["ParkingSession"]] = relationship(
        back_populates="rate", lazy="raise"
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_rate_name"),
        CheckConstraint("price_per_hour > 0", name="ck_positive_price_per_hour"),
        CheckConstraint("minimum_charge >= 0", name="ck_non_negative_minimum_charge"),
    )
