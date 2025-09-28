from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from domain.posts import entities

from . import dtos

Entity = TypeVar("Entity")
CreateDto = TypeVar("CreateDto")
ReadAllDto = TypeVar("ReadAllDto")


class CRUDRepository(Generic[Entity, CreateDto, ReadAllDto], metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: CreateDto) -> Entity: ...

    @abstractmethod
    async def read(self, entity_id: int) -> Entity: ...

    @abstractmethod
    async def update(self, entity: Entity) -> Entity: ...

    @abstractmethod
    async def delete(self, entity: Entity) -> Entity: ...

    @abstractmethod
    async def read_all(self, dto: ReadAllDto) -> list[Entity]: ...


class PostsRepository(
    CRUDRepository[entities.Post, dtos.CreatePostDto, dtos.ReadAllPostsDto],
    metaclass=ABCMeta,
):
    @abstractmethod
    async def read_by_category(self, category_id: int) -> list[entities.Post]: ...


class CategoriesRepository(
    CRUDRepository[
        entities.Category, dtos.CreateCategoryDto, dtos.ReadAllCategoriesDto
    ],
    metaclass=ABCMeta,
):
    pass
