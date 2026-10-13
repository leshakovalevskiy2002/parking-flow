from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from app.models import Fine


class FinesRepository:
    def __init__(self, session):
        self.session = session

    async def create_fine(
        self,
        car_number: str,
        inspector_id: UUID,
        reason: str,
        amount: Decimal,
        idempotency_key: str,
    ) -> Fine:
        fine = Fine(
            car_number=car_number,
            reason=reason,
            amount=amount,
            issued_by_id=inspector_id,
            idempotency_key=idempotency_key,
        )
        self.session.add(fine)
        await self.session.flush()
        return fine

    async def get_by_idempotency_key(self, idempotency_key: str) -> Fine | None:
        query = select(Fine).where(Fine.idempotency_key == idempotency_key)
        result = await self.session.scalars(query)
        return result.one_or_none()
