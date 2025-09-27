from application.posts import dtos
from application.posts.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    PostAlreadyExistsError,
    PostNotFoundError,
)
from application.posts.repositories import CategoriesRepository, PostsRepository
from domain.posts import entities

from ..repositories.config import MapperConfig
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

    _mapper = MapperConfig(
        create_mapper=mappers.post__create_mapper,
        entity_mapper=mappers.post__map_from_db,
        model_mapper=mappers.post__map_to_db,
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

    _mapper = MapperConfig(
        create_mapper=mappers.category__create_mapper,
        entity_mapper=mappers.category__map_from_db,
        model_mapper=mappers.category__map_to_db,
    )
