from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from sqlalchemy import Delete, Insert, Select, Update, insert, select
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import Executable

from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError

Id = TypeVar("Id")
CreateDto = TypeVar("CreateDto")
ReadAllDto = TypeVar("ReadAllDto")

Entity = TypeVar("Entity")
ModelType = TypeVar("ModelType")
NotFoundException = TypeVar("NotFoundException", bound=EntityNotFoundError)
AlreadyExistsException = TypeVar(
    "AlreadyExistsException", bound=EntityAlreadyExistsError
)

EntityMapper = Callable[[ModelType], Entity]
ModelMapper = Callable[[Entity], ModelType]
CreateMapper = Callable[[CreateDto], ModelType]


@dataclass
class PostgresRepositoryConfig(Generic[ModelType, Entity, Id, CreateDto]):
    model: type[ModelType]
    entity: type[Entity]
    entity_mapper: Callable[[ModelType], Entity]
    model_mapper: Callable[[Entity], ModelType]
    create_model_mapper: Callable[[CreateDto], ModelType]
    not_found_exception: type[EntityNotFoundError] = EntityNotFoundError
    already_exists_exception: type[EntityAlreadyExistsError] = EntityAlreadyExistsError

    def extract_id_from_entity(self, entity: Entity) -> Id:  # noqa: PEP-484
        return entity.id

    def extract_id_from_model(self, model: ModelType) -> Id:  # noqa: PEP-484
        return model.id

    def add_options(self, statement: Executable) -> Executable:
        return statement.options(*self.get_options())

    def get_options(self) -> list[LoaderOption]:  # noqa: PEP-484
        return []

    @staticmethod
    def _model_to_dict(model: ModelType) -> dict:
        return {
            column.key: getattr(model, column.key)
            for column in model.__table__.columns
            if getattr(model, column.key) is not None
        }

    def get_select_query(self, model_id: Id) -> Select:
        return self._add_where_id(select(self.model), model_id)

    def get_default_select_all_query(self, ids: list[Id]) -> Select:
        return select(self.model).where(self.model.id.in_(ids)).order_by(self.model.id)

    def get_select_all_query(self, _: Any) -> Select:
        return select(self.model).order_by(self.model.id)

    def get_insert_many_query(self, models: list[ModelType]) -> Insert:
        return (
            insert(self.model)
            .values(list(map(self._model_to_dict, models)))
            .returning(self.model)
        )

    def _add_where_id(
        self, statement: Select | Update | Delete, model_id: Id
    ) -> Select | Update | Delete:
        return statement.where(self.model.id == model_id)


class CRUDRepositoryConfig(
    Generic[
        CreateDto,
        ReadAllDto,
        Entity,
        ModelType,
        NotFoundException,
        AlreadyExistsException,
        CreateMapper,
        EntityMapper,
        ModelMapper,
    ],
    PostgresRepositoryConfig,
):
    """Конфигурация репозитория пользователей."""

    def __init__(self):
        """Инициализирует конфигурацию маппинга пользователей."""

        super().__init__(
            model=ModelType,
            entity=Entity,
            entity_mapper=EntityMapper,
            model_mapper=ModelMapper,
            create_model_mapper=CreateMapper,
            not_found_exception=NotFoundException,
            already_exists_exception=AlreadyExistsException,
        )

    def get_select_all_query(self, dto: ReadAllDto) -> Select:
        return (
            select(self.model)
            .order_by(self.model.id)
            .offset(dto.page * dto.page_size)
            .limit(dto.page_size)
        )
