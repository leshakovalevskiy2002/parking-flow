from collections.abc import AsyncIterator

from app.config.settings import async_session_maker
from app.uow import UnitOfWork


async def get_unit_of_work() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(async_session_maker) as uow:
        yield uow
