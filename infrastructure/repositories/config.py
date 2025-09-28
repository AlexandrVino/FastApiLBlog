from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, get_args, get_origin

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


@dataclass
class MapperConfig:
    create_mapper: Callable[[CreateDto], ModelType]
    entity_mapper: Callable[[ModelType], Entity]
    model_mapper: Callable[[Entity], ModelType]


@dataclass
class CRUDRepositoryConfig(
    Generic[
        CreateDto,
        ReadAllDto,
        Entity,
        ModelType,
        NotFoundException,
        AlreadyExistsException,
    ]
):
    read_all_dto: type[ReadAllDto]
    model: type[ModelType]
    entity: type[Entity]
    entity_mapper: Callable[[ModelType], Entity]
    model_mapper: Callable[[Entity], ModelType]
    create_mapper: Callable[[CreateDto], ModelType]
    not_found_exception: type[NotFoundException] = NotFoundException
    already_exists_exception: type[AlreadyExistsException] = AlreadyExistsException

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

    def get_select_all_query(self, dto: ReadAllDto) -> Select:
        query = select(self.model).order_by(self.model.id)
        if getattr(dto, "page") is int and getattr(dto, "page_size") is int:
            query = query.offset(dto.page * dto.page_size).limit(dto.page_size)

        return query

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
        return statement.where(self.model.id == model_id)  # type: ignore
