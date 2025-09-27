from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.posts.services import PostsService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[dtos.PostModel])
async def read_all(
    actor: Annotated[User, Depends(get_user)], posts: FromDishka[PostsService]
):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return map(mappers.post__map_to_pydantic, await posts.read_all(None, actor))


@router.get("/{post_id}", response_model=dtos.PostModel)
async def read(
    post_id: int,
    actor: Annotated[User, Depends(get_user)],
    posts: FromDishka[PostsService],
):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.post__map_to_pydantic(await posts.read(post_id, actor))
