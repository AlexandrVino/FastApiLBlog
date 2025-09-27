from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Наследует функциональность асинхронных атрибутов и предоставляет
    базовую конфигурацию для декларативного определения моделей.
    Включает соглашение об именовании для ограничений базы данных.
    """

    metadata = MetaData(naming_convention=constraint_naming_conventions)


def get_engine(url: str) -> AsyncEngine:
    """Создает и возвращает асинхронный движок SQLAlchemy."""

    return create_async_engine(url, pool_size=32)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """Создает фабрику асинхронных сессий SQLAlchemy."""

    return async_sessionmaker(bind=engine, expire_on_commit=False)
