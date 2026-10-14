from datetime import datetime
from decimal import Decimal
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.core.enums import FineStatus
from app.domain.errors import CarIsParkedLegallyError
from app.models import Fine, User
from app.uow import UnitOfWork


class FinesService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_fine(self, inspector: User, car_number: str, idempotency_key: str) -> Fine:
        active_session = await self.uow.parking_sessions.get_active_session_by_car_number(
            car_number
        )

        if active_session:
            raise CarIsParkedLegallyError(car_number)

        existing = await self.uow.fines.get_by_idempotency_key(idempotency_key)
        if existing:
            return existing

        fine_for_parked_without_session = Decimal("25.00")

        try:
            return await self.uow.fines.create_fine(
                car_number=car_number,
                inspector_id=inspector.id,
                reason="No parking session",
                amount=fine_for_parked_without_session,
                idempotency_key=idempotency_key,
            )
        except IntegrityError as exc:
            await self.uow.rollback()
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__

            if isinstance(original_exception, UniqueViolationError):
                existing = await self.uow.fines.get_by_idempotency_key(idempotency_key)
                if existing:
                    return existing
            raise

    async def get_fines(
        self,
        user_id: UUID | None,
        car_number: str | None,
        status: FineStatus | None,
        from_date: datetime | None,
        to_date: datetime | None,
        page: int,
        size: int,
        inspector_id: UUID | None = None,
    ):
        filters = []
        if user_id is not None:
            filters.append(Fine.user_id == user_id)
        if car_number is not None:
            filters.append(Fine.car_number == car_number.upper())
        if status is not None:
            filters.append(Fine.status == status)
        if from_date is not None:
            filters.append(Fine.issued_at >= from_date)
        if to_date is not None:
            filters.append(Fine.issued_at <= to_date)
        if inspector_id is not None:
            filters.append(Fine.issued_by_id == inspector_id)

        items, total = await self.uow.fines.get_fines(
            filters=filters,
            page=page,
            size=size,
            order_by=Fine.issued_at.asc(),
        )

        return {"items": items, "total": total, "page": page, "size": size}
