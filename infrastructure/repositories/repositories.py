import traceback
from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Optional

from sqlalchemy import Insert, Select, Update, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .config import CreateModelType, Entity, Id, ModelType, PostgresRepositoryConfig


class SessionMixin:
    """Миксин для работы с сессией"""

    _session: AsyncSession

    def _should_commit(self) -> bool:
        return not self._session.in_nested_transaction()


class ConfigMixin(Generic[ModelType, Entity, Id, CreateModelType]):
    """Миксин для работы с конфигурацией"""

    _config: PostgresRepositoryConfig

    async def get_scalar_or_none(self, query: Select) -> Optional[ModelType]:
        return (
            await self._session.execute(self._config.add_options(query))
        ).scalar_one_or_none()

    async def get_entities_from_query(
        self, query: Select | Update | Insert
    ) -> list[Entity]:
        result = await self._session.scalars(self._config.add_options(query))
        return [self._config.entity_mapper(model) for model in result.unique().all()]

    async def _get_entity_by_id(self, model_id: Id) -> Entity:
        if model := await self._session.get(
            self._config.model,
            model_id,
            options=self._config.get_options(),
            populate_existing=True,
        ):
            return self._config.entity_mapper(model)
        raise self._config.not_found_exception()


class CreateMixin(
    SessionMixin, ConfigMixin, Generic[ModelType, Entity, CreateModelType]
):
    """Миксин для операций создания"""

    async def _create_models(self, models: list[ModelType]) -> list[Entity]:
        try:
            query = self._config.get_insert_many_query(models)
            return await self.get_entities_from_query(query)
        except IntegrityError:
            traceback.print_exc()
            raise self._config.already_exists_exception()

    async def create(self, model: ModelType) -> Entity:
        try:
            self._session.add(model)
            if self._should_commit():
                await self._session.commit()
            await self._session.merge(model)

            # Получаем ID созданной модели и возвращаем полную сущность
            model_id = self._config.extract_id_from_model(model)
            return await self._get_entity_by_id(model_id)
        except IntegrityError:
            traceback.print_exc()
            raise self._config.already_exists_exception()

    async def create_from_dto(self, dto: CreateModelType) -> Entity:
        return await self.create(self._config.create_model_mapper(dto))

    async def create_from_entity(self, entity: Entity) -> Entity:
        return await self.create(self._config.model_mapper(entity))

    async def create_many_from_dto(self, dtos: list[CreateModelType]) -> list[Entity]:
        models = [self._config.create_model_mapper(dto) for dto in dtos]
        return await self._create_models(models)

    async def create_many_from_entity(self, entities: list[Entity]) -> list[Entity]:
        models = [self._config.model_mapper(entity) for entity in entities]
        return await self._create_models(models)

    async def bulk_insert(self, entities: list[Entity]) -> list[Entity]:
        return await self.create_many_from_entity(entities)


class ReadMixin(SessionMixin, ConfigMixin, Generic[ModelType, Entity, Id]):
    """Миксин для операций чтения"""

    async def read(self, model_id: Id) -> Entity:
        return await self._get_entity_by_id(model_id)

    async def read_all(self, dto: Any = None) -> list[Entity]:
        return await self.get_entities_from_query(
            self._config.get_select_all_query(dto)
        )

    async def read_by_ids(self, model_ids: list[Id]) -> list[Entity]:
        return await self.get_entities_from_query(
            self._config.get_default_select_all_query(model_ids)
        )

    async def exists(self, model_id: Id) -> bool:
        query = select(self._config.model.id).where(self._config.model.id == model_id)
        return await self.get_scalar_or_none(query) is not None

    async def count(self, dto: Any = None) -> int:
        query = text("SELECT COUNT(*) FROM {}".format(self._config.model.__tablename__))
        result = await self._session.execute(query)
        return result.scalar_one_or_none() or 0


class UpdateMixin(SessionMixin, ConfigMixin, Generic[ModelType, Entity]):
    """Миксин для операций обновления"""

    async def update(self, entity: Entity) -> Entity:
        model = self._config.model_mapper(entity)
        await self._session.merge(model)
        if self._should_commit():
            await self._session.commit()
        return self._config.entity_mapper(model)

    async def bulk_update(self, entities: list[Entity]) -> list[Entity]:
        updated_entities = []
        for entity in entities:
            updated_entities.append(await self.update(entity))
        return updated_entities

    async def update_by_query(self, query: Update) -> Entity:
        result = await self._session.scalar(self._config.add_options(query))
        if self._should_commit():
            await self._session.commit()
        return self._config.entity_mapper(result)

    async def bulk_update_by_query(self, query: Update) -> list[Entity]:
        results = await self._session.scalars(self._config.add_options(query))
        if self._should_commit():
            await self._session.commit()
        return list(map(self._config.entity_mapper, results))


class DeleteMixin(SessionMixin, ConfigMixin, Generic[ModelType, Entity]):
    """Миксин для операций удаления"""

    async def delete(self, entity: Entity) -> Entity:
        if model := await self._session.get(
            self._config.model, self._config.extract_id_from_entity(entity)
        ):
            await self._session.delete(model)
            if self._should_commit():
                await self._session.commit()
            return entity
        raise self._config.not_found_exception()

    async def delete_by_id(self, model_id: Id) -> Entity:
        entity = await self._get_entity_by_id(model_id)
        return await self.delete(entity)

    async def bulk_delete(self, entities: list[Entity]) -> list[Entity]:
        deleted_entities = []
        for entity in entities:
            deleted_entities.append(await self.delete(entity))
        return deleted_entities

    async def truncate(self):
        """Очищает всю таблицу (удаляет все записи)"""
        table_name = self._config.model.__tablename__
        await self._session.execute(
            text(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE')
        )
        if self._should_commit():
            await self._session.commit()


class BaseRepository(metaclass=ABCMeta):
    @abstractmethod
    def _should_commit(self) -> bool:
        pass


class PostgresRepository(
    BaseRepository,
    CreateMixin[ModelType, Entity, CreateModelType],
    ReadMixin[ModelType, Entity, Id],
    UpdateMixin[ModelType, Entity],
    DeleteMixin[ModelType, Entity],
    Generic[ModelType, Entity, Id, CreateModelType],
):
    def __init__(self, session: AsyncSession, config: PostgresRepositoryConfig):
        self._session = session
        self._config = config

    def _should_commit(self) -> bool:
        return not self._session.in_nested_transaction()
