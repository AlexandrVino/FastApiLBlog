import traceback
from typing import Any, Generic

from sqlalchemy import Insert, Select, Update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .config import (
    AlreadyExistsException,
    CreateDto,
    CRUDRepositoryConfig,
    Entity,
    Id,
    ModelType,
    NotFoundException,
    ReadAllDto,
)


class PostgresRepository:
    config: CRUDRepositoryConfig

    def __init__(self, session: AsyncSession, config: CRUDRepositoryConfig):
        self.session = session
        self.config = config

    async def _create_models(self, models: list[ModelType]) -> list[Entity]:
        try:
            self.session.add_all(models)
            await self.session.flush()
            for m in models:
                await self.session.refresh(m)
            return [self.config.entity_mapper(m) for m in models]
        except IntegrityError:
            traceback.print_exc()
            raise self.config.already_exists_exception()

    async def create(self, model: ModelType) -> Entity:
        try:
            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model)
            return self.config.entity_mapper(model)
        except IntegrityError:
            traceback.print_exc()
            raise self.config.already_exists_exception()

    async def get_scalar_or_none(self, query: Select) -> ModelType | None:
        return (
            await self.session.execute(self.config.add_options(query))
        ).scalar_one_or_none()

    async def get_entities_from_query(
        self, query: Select | Update | Insert
    ) -> list[Entity]:
        result = await self.session.scalars(self.config.add_options(query))
        return [self.config.entity_mapper(model) for model in result.unique().all()]

    async def read(self, model_id: Id) -> Entity:
        if model := await self.session.get(
            self.config.model,
            model_id,
            options=self.config.get_options(),
            populate_existing=True,
        ):
            return self.config.entity_mapper(model)
        raise self.config.not_found_exception()

    async def read_all(self, dto: Any = None) -> list[Entity]:
        return await self.get_entities_from_query(self.config.get_select_all_query(dto))

    async def read_by_ids(self, model_ids: list[Id]) -> list[Entity]:
        return await self.get_entities_from_query(
            self.config.get_default_select_all_query(model_ids)
        )

    async def create_from_dto(self, dto: CreateDto) -> Entity:
        return await self.create(self.config.create_mapper(dto))

    async def create_from_entity(self, entity: Entity) -> Entity:
        return await self.create(self.config.model_mapper(entity))

    async def create_many_from_dto(self, dtos: list[CreateDto]) -> list[Entity]:
        models = [self.config.create_mapper(dto) for dto in dtos]
        return await self._create_models(models)

    async def create_many_from_entity(self, entities: list[Entity]) -> list[Entity]:
        models = [self.config.model_mapper(e) for e in entities]
        return await self._create_models(models)

    async def update(self, entity: Entity) -> Entity:
        model = self.config.model_mapper(entity)
        merged = await self.session.merge(model)
        await self.session.flush()
        await self.session.refresh(merged)
        return self.config.entity_mapper(merged)

    async def delete(self, entity: Entity) -> Entity:
        model = await self.session.get(
            self.config.model, self.config.extract_id_from_entity(entity)
        )
        if not model:
            raise self.config.not_found_exception()
        await self.session.delete(model)
        await self.session.flush()
        return entity


class CRUDDatabaseRepository(
    Generic[
        CreateDto,
        ReadAllDto,
        Entity,
        ModelType,
        NotFoundException,
        AlreadyExistsException,
    ],
):
    """Репозиторий для работы с пользователями в базе данных."""

    _config: CRUDRepositoryConfig

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий пользователей."""

        self._repository = PostgresRepository(session, self._config)

    # region queries
    async def read_all(self, dto: ReadAllDto) -> list[Entity]:
        """Возвращает список пользователей с пагинацией."""

        return await self._repository.read_all(dto)

    async def read(self, entity_id: int) -> Entity:
        """Возвращает пользователя по идентификатору."""

        return await self._repository.read(entity_id)

    # endregion
    # region command
    async def create(self, dto: ReadAllDto) -> Entity:
        """Создает нового пользователя с паролем."""

        return await self._repository.create(self._config.create_mapper(dto))

    async def update(self, entity: Entity) -> Entity:
        """Обновляет данные пользователя."""

        return await self._repository.update(entity)

    async def delete(self, entity: Entity) -> Entity:
        """Удаляет пользователя."""

        return await self._repository.delete(entity)

    # endregion
