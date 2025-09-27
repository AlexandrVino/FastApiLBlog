import asyncio
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ..config import Config
from ..postgres import get_engine, get_session_maker
from ..transactions import TransactionsDatabaseGateway, TransactionsGateway


class DatabaseProvider(Provider):
    """
    Провайдер зависимостей для работы с базой данных.

    Предоставляет зависимости для подключения к PostgreSQL, управления сессиями
    и транзакциями с различными областями видимости (scope).
    """

    @provide(scope=Scope.APP)
    def get_engine(self, config: Config) -> AsyncEngine:
        """Создает и предоставляет асинхронный движок SQLAlchemy."""

        return get_engine(str(config.postgres_url))

    @provide(scope=Scope.APP)
    def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker:
        """Предоставляет фабрику сессий SQLAlchemy."""

        return get_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        """Предоставляет асинхронную сессию для работы с БД."""

        async with session_maker(expire_on_commit=False) as session:
            yield session
            await session.commit()
        await asyncio.shield(session.close())

    @provide(scope=Scope.REQUEST)
    async def get_transaction(self, session: AsyncSession) -> TransactionsGateway:
        """Предоставляет шлюз для управления транзакциями."""

        return TransactionsDatabaseGateway(session)
