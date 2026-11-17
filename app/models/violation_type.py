from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ViolationType(Base):
    code: Mapped[str] = mapped_column(String(100), unique=True)
    reason: Mapped[str] = mapped_column(Text)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    __table_args__ = (CheckConstraint("amount > 0", name="ck_positive_violation_amount"),)
