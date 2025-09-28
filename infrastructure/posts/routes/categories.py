from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from application.posts.services import CategoriesService, PostsService
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[dtos.CategoryModel])
async def read_all(categories: FromDishka[CategoriesService]):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return map(mappers.category__map_to_pydantic, await categories.read_all(None))


@router.get("/{category_id}", response_model=dtos.CategoryModel)
async def read(
    category_id: int,
    categories: FromDishka[CategoriesService],
):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.category__map_to_pydantic(await categories.read(category_id))


@router.get("/{category_id}/posts", response_model=list[dtos.PostModel])
async def read(
    category_id: int,
    posts: FromDishka[PostsService],
):
    """Возвращает данные текущего аутентифицированного пользователя."""
    return map(mappers.post__map_to_pydantic, await posts.read_by_category(category_id))
