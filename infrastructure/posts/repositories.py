from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from application.posts import dtos
from application.posts.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    PostAlreadyExistsError,
    PostNotFoundError,
)
from application.posts.repositories import CategoriesRepository, PostsRepository
from domain.posts import entities

from ..repositories.config import CRUDRepositoryConfig, ReadAllDto
from ..repositories.repositories import CRUDDatabaseRepository
from . import mappers
from .models import CategoryDatabaseModel, PostDatabaseModel


class PostsDatabaseRepository(
    CRUDDatabaseRepository[
        dtos.CreatePostDto,
        dtos.ReadAllPostsDto,
        entities.Post,
        PostDatabaseModel,
        PostNotFoundError,
        PostAlreadyExistsError,
    ],
    PostsRepository,
):
    """Репозиторий для работы с постами в базе данных."""

    class RepositoryConfig(CRUDRepositoryConfig):
        def __init__(self):
            super().__init__(
                read_all_dto=dtos.ReadAllPostsDto,
                model=PostDatabaseModel,
                entity=entities.Post,
                create_mapper=mappers.post__create_mapper,
                entity_mapper=mappers.post__map_from_db,
                model_mapper=mappers.post__map_to_db,
                not_found_exception=PostNotFoundError,
                already_exists_exception=PostAlreadyExistsError,
            )

        def get_options(self) -> list[LoaderOption]:
            return [selectinload(self.model.category)]

        def get_select_all_by_category_query(self, category_id: int) -> Select:
            return (
                select(self.model)
                .order_by(self.model.id)
                .where(self.model.category_id == category_id)
            )

    _config = RepositoryConfig()

    async def read_by_category(self, category_id: int) -> list[entities.Post]:
        return await self._repository.get_entities_from_query(
            self._config.get_select_all_by_category_query(category_id)
        )


class CategoriesDatabaseRepository(
    CRUDDatabaseRepository[
        dtos.CreateCategoryDto,
        dtos.ReadAllCategoriesDto,
        entities.Category,
        CategoryDatabaseModel,
        CategoryNotFoundError,
        CategoryAlreadyExistsError,
    ],
    CategoriesRepository,
):
    """Репозиторий для работы с категориями в базе данных."""

    _config = CRUDRepositoryConfig(
        read_all_dto=dtos.ReadAllCategoriesDto,
        model=CategoryDatabaseModel,
        entity=entities.Category,
        create_mapper=mappers.category__create_mapper,
        entity_mapper=mappers.category__map_from_db,
        model_mapper=mappers.category__map_to_db,
        not_found_exception=CategoryNotFoundError,
        already_exists_exception=CategoryAlreadyExistsError,
    )
