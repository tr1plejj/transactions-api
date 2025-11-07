from typing import Any, AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from src.settings import settings
from src.uow import UnitOfWork, AbstractUnitOfWork


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_database_engine(self) -> AsyncEngine:
        return create_async_engine(settings.database_url)

    @provide(scope=Scope.APP)
    def provide_database_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def provide_uow(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AbstractUnitOfWork, Any]:
        uow = UnitOfWork(session_factory=sessionmaker)
        async with uow:
            yield uow
