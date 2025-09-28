from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ..config import Config
from ..postgres import get_engine, get_session_maker
from ..transactions import TransactionsDatabaseGateway, TransactionsGateway


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: Config) -> AsyncEngine:
        return get_engine(str(config.postgres_url))

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return get_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        session: AsyncSession = session_maker(expire_on_commit=False)
        try:
            async with session.begin():
                yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    async def get_transaction(self, session: AsyncSession) -> TransactionsGateway:
        """Предоставляет шлюз для управления транзакциями."""

        return TransactionsDatabaseGateway(session)
