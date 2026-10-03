import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class TimeStampedMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid4, server_default=text("gen_random_uuid()")
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
        onupdate=lambda: datetime.now(UTC),
    )


class Base(TimeStampedMixin, DeclarativeBase):
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", cls.__name__).lower() + "s"
