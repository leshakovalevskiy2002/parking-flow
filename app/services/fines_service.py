from decimal import Decimal

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

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
