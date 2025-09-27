from application.posts import dtos
from application.posts.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    PostAlreadyExistsError,
    PostNotFoundError,
)
from application.posts.repositories import CategoriesRepository
from domain.posts import entities

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
        mappers.post__create_mapper,
        mappers.post__map_from_db,
        mappers.post__map_to_db,
    ]
):
    """Репозиторий для работы с постами в базе данных."""


class CategoriesDatabaseRepository(
    CRUDDatabaseRepository[
        dtos.CreateCategoryDto,
        dtos.ReadAllCategoriesDto,
        entities.Category,
        CategoryDatabaseModel,
        CategoryNotFoundError,
        CategoryAlreadyExistsError,
        mappers.category__create_mapper,
        mappers.category__map_from_db,
        mappers.category__map_to_db,
    ],
    CategoriesRepository,
):
    """Репозиторий для работы с категориями в базе данных."""
