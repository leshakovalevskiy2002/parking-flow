from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ParkingSessionStatus
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.parking_place import ParkingPlace
    from app.models.rate import Rate
    from app.models.user import User


class ParkingSession(Base):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    place_id: Mapped[UUID] = mapped_column(
        ForeignKey("parking_places.id", ondelete="RESTRICT"), index=True
    )
    rate_id: Mapped[UUID] = mapped_column(ForeignKey("rates.id", ondelete="RESTRICT"))
    car_number: Mapped[str] = mapped_column(String(16), index=True)

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        server_default=func.now(),
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    total_cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    status: Mapped[ParkingSessionStatus] = mapped_column(
        Enum(ParkingSessionStatus, name="parking_session_status_enum"),
        server_default=ParkingSessionStatus.ACTIVE.value,
    )

    hourly_rate_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    minimum_charge_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    user: Mapped["User"] = relationship(back_populates="parking_sessions")
    parking_place: Mapped["ParkingPlace"] = relationship(back_populates="parking_sessions")
    rate: Mapped["Rate"] = relationship(back_populates="parking_sessions")

    __table_args__ = (
        CheckConstraint("end_time IS NULL OR end_time >= start_time", name="end_after_start_time"),
        CheckConstraint("total_cost IS NULL OR total_cost > 0", name="ck_total_cost"),
        CheckConstraint("hourly_rate_snapshot > 0", name="ck_hourly_rate_snapshot"),
        CheckConstraint("minimum_charge_snapshot >= 0", name="ck_minimum_charge_snapshot"),
    )
