from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ParkingPlaceStatus, ParkingPlaceType
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.parking_session import ParkingSession


class ParkingPlace(Base):
    number: Mapped[str] = mapped_column(String(12))
    type: Mapped[ParkingPlaceType] = mapped_column(
        "place_type",
        Enum(ParkingPlaceType, name="parking_type_enum"),
        server_default=ParkingPlaceType.REGULAR.value,
    )
    status: Mapped[ParkingPlaceStatus] = mapped_column(
        Enum(ParkingPlaceStatus, name="parking_status_enum"),
        server_default=ParkingPlaceStatus.FREE.value,
    )

    parking_sessions: Mapped[list["ParkingSession"]] = relationship(back_populates="parking_place")

    __table_args__ = (UniqueConstraint("number", name="uq_parking_place_number"),)
