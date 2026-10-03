from datetime import datetime
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
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import FineStatus
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Fine(Base):
    car_number: Mapped[str] = mapped_column(String(16), index=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(Text)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    issued_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), index=True
    )
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[FineStatus] = mapped_column(
        Enum(FineStatus, name="fine_status_enum"),
        server_default=FineStatus.UNPAID.value,
    )

    issued_by: Mapped["User"] = relationship(
        back_populates="issued_fines", foreign_keys=[issued_by_id]
    )
    user: Mapped["User | None"] = relationship(back_populates="user_fines", foreign_keys=[user_id])

    __table_args__ = (CheckConstraint("amount > 0", "positive_fine_amount"),)
