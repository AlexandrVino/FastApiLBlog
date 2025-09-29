from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.posts.services import PostsService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=dtos.PostModelDetail)
async def create_post(
    dto: dtos.CreatePostDto,
    actor: Annotated[User, Depends(get_user)],
    posts: FromDishka[PostsService],
):
    return mappers.post__map_to_pydantic_detail(
        await posts.create(mappers.post__create_dto_mapper(dto), actor)
    )


@router.put("/{post_id}", response_model=dtos.PostModelDetail)
async def update_post(
    post_id: int,
    dto: dtos.UpdatePostDto,
    actor: Annotated[User, Depends(get_user)],
    posts: FromDishka[PostsService],
):
    return mappers.post__map_to_pydantic_detail(
        await posts.update(mappers.post__map_update_dto(dto, post_id), actor)
    )


@router.delete("/{post_id}", response_model=dtos.PostModelDetail)
async def delete_post(
    post_id: int,
    actor: Annotated[User, Depends(get_user)],
    posts: FromDishka[PostsService],
):
    return mappers.post__map_to_pydantic_detail(await posts.delete(post_id, actor))
