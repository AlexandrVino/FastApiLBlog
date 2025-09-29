from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from application.posts.services import PostsService
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[dtos.PostModel])
async def read_all(posts: FromDishka[PostsService]):
    return map(mappers.post__map_to_pydantic, await posts.read_all(None))


@router.get("/{post_id}", response_model=dtos.PostModelDetail)
async def read(
    post_id: int,
    posts: FromDishka[PostsService],
):
    return mappers.post__map_to_pydantic_detail(await posts.read(post_id))
