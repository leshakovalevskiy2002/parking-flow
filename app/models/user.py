from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import UserRole, UserStatus
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.fine import Fine
    from app.models.parking_session import ParkingSession


class User(Base):
    email: Mapped[str] = mapped_column(String(100), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"),
        server_default=UserRole.USER.value,
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status_enum"),
        server_default=UserStatus.ACTIVE.value,
    )

    parking_sessions: Mapped[list["ParkingSession"]] = relationship(back_populates="user")
    issued_fines: Mapped[list["Fine"]] = relationship(back_populates="issued_by")
    user_fines: Mapped[list["Fine"]] = relationship(back_populates="user")

    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)
