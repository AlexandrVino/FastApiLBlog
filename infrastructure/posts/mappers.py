from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, link_function

from application.posts import dtos
from domain.posts.entities import Category, Post
from infrastructure.mappers import postgres_retort, pydantic_retort

from . import dtos as models
from .models import CategoryDatabaseModel, PostDatabaseModel

pgsql_retort = postgres_retort.extend(recipe=[])
py_retort = pydantic_retort.extend(recipe=[])

category__map_from_db = pgsql_retort.get_converter(
    CategoryDatabaseModel,
    Category,
    recipe=[
        allow_unlinked_optional(P[models.Category].posts),
    ],
)
category__map_to_db = pgsql_retort.get_converter(Category, CategoryDatabaseModel)
category__create_mapper = pgsql_retort.get_converter(
    models.CreateCategoryDto,
    CategoryDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[CategoryDatabaseModel].id),
        allow_unlinked_optional(P[CategoryDatabaseModel].created_at),
        allow_unlinked_optional(P[CategoryDatabaseModel].updated_at),
    ],
)
category__map_to_pydantic = py_retort.get_converter(
    Category,
    models.CategoryModel,
)


@py_retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, category_id: category_id,
            P[models.UpdateCategoryDto].id,
        )
    ]
)
def category__map_update_dto(
    dto: models.UpdateCategoryDto, category_id: int
) -> dtos.UpdateCategoryDto: ...


post__map_from_db = pgsql_retort.get_converter(
    PostDatabaseModel,
    Post,
    recipe=[
        coercer(
            CategoryDatabaseModel,
            Category,
            category__map_from_db,
        ),
    ],
)
post__map_to_db = pgsql_retort.get_converter(
    Post,
    PostDatabaseModel,
    recipe=[
        link_function(
            lambda post: post.category.id,
            P[PostDatabaseModel].category_id,
        ),
        coercer(
            Category,
            CategoryDatabaseModel,
            category__map_to_db,
        ),
    ],
)
post__create_mapper = pgsql_retort.get_converter(
    models.CreatePostDto,
    PostDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[PostDatabaseModel].id),
        allow_unlinked_optional(P[PostDatabaseModel].created_at),
        allow_unlinked_optional(P[PostDatabaseModel].updated_at),
        allow_unlinked_optional(P[PostDatabaseModel].category),
    ],
)
post__map_to_pydantic = py_retort.get_converter(
    Post,
    models.PostModel,
    recipe=[coercer(Category, models.CategoryModel, category__map_to_pydantic)],
)


@py_retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, user_id: user_id,
            P[models.UpdatePostDto].id,
        )
    ]
)
def post__map_update_dto(
    dto: models.UpdatePostDto, post_id: int
) -> dtos.UpdatePostDto: ...
