from decimal import Decimal

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from app.models import Rate
from app.services.exceptions.rates import RateAlreadyExistsError, RateInUseError, RateNotExistsError
from app.uow import UnitOfWork


class RateService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_rate(
        self, name: str, price_per_hour: Decimal, minimum_charge: Decimal
    ) -> Rate:
        existing = await self.uow.rates.get_by_name(name)

        if existing:
            raise RateAlreadyExistsError(name)

        try:
            return await self.uow.rates.create(name, price_per_hour, minimum_charge)
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__

            if isinstance(original_exception, UniqueViolationError):
                raise RateAlreadyExistsError(name) from exc
            raise

    async def get_rate_by_name(self, name: str) -> Rate:
        rate = await self.uow.rates.get_by_name(name.capitalize())

        if rate is None:
            raise RateNotExistsError(name)
        return rate

    async def update_rate(
        self,
        name: str,
        new_name: str | None,
        new_price_per_hour: Decimal | None,
        new_minimum_charge: Decimal | None,
    ) -> Rate:
        rate = await self.get_rate_by_name(name)

        if new_name is not None:
            rate.name = new_name

        if new_price_per_hour is not None:
            rate.price_per_hour = new_price_per_hour

        if new_minimum_charge is not None:
            rate.minimum_charge = new_minimum_charge

        try:
            await self.uow.flush()
        except IntegrityError as exc:
            if exc.orig is None:
                raise

            original_exception = exc.orig.__cause__
            if isinstance(original_exception, UniqueViolationError):
                raise RateAlreadyExistsError(rate.name) from exc
            raise

        return rate

    async def delete_rate(self, name: str) -> None:
        rate = await self.get_rate_by_name(name)

        if await self.uow.parking_sessions.exists_by_rate_id(rate.id):
            raise RateInUseError(name)

        rate.is_active = False
        await self.uow.flush()
