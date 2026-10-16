from decimal import Decimal
from uuid import UUID

from sqlalchemy import ColumnElement, UnaryExpression, func, select

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

    async def get_fines(
        self, filters: list[ColumnElement[bool]], page: int, size: int, order_by: UnaryExpression
    ) -> tuple[list[Fine], int]:
        base_query = select(Fine)
        if filters:
            base_query = base_query.where(*filters)

        count_query = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()

        items_query = base_query.order_by(order_by).offset((page - 1) * size).limit(size)
        result = await self.session.scalars(items_query)
        items = list(result.all())
        return items, total
