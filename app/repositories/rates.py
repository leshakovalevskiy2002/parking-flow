from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rate import Rate


class RateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rates(self):
        result = await self.session.scalars(select(Rate).where(Rate.is_active.is_(True)))
        return result.all()

    async def get_by_name(self, name: str) -> Rate | None:
        query = select(Rate).where(Rate.name == name, Rate.is_active.is_(True))
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def create(self, name: str, price_per_hour: Decimal, minimum_charge: Decimal) -> Rate:
        rate = Rate(name=name, price_per_hour=price_per_hour, minimum_charge=minimum_charge)
        self.session.add(rate)
        await self.session.flush()
        return rate
