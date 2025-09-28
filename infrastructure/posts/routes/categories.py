from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.posts.services import CategoriesService, PostsService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[dtos.CategoryModel])
async def read_all(
    actor: Annotated[User, Depends(get_user)], categories: FromDishka[CategoriesService]
):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return map(
        mappers.category__map_to_pydantic, await categories.read_all(None, actor)
    )


@router.get("/{category_id}", response_model=dtos.CategoryModel)
async def read(
    category_id: int,
    actor: Annotated[User, Depends(get_user)],
    categories: FromDishka[CategoriesService],
):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.category__map_to_pydantic(await categories.read(category_id, actor))


@router.get("/{category_id}/posts", response_model=list[dtos.PostModel])
async def read(
    category_id: int,
    actor: Annotated[User, Depends(get_user)],
    posts: FromDishka[PostsService],
):
    """Возвращает данные текущего аутентифицированного пользователя."""
    return map(
        mappers.post__map_to_pydantic, await posts.read_by_category(category_id, actor)
    )
