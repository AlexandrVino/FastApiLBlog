from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.users.dtos import ReadAllUsersDto
from application.users.services import UsersService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.models import ErrorModel
from infrastructure.users import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[dtos.UserModel])
async def read_all_users(
    users: FromDishka[UsersService],
    actor: Annotated[User, Depends(get_user)],
    page: int = 0,
    page_size: int = 50,
):
    """Получает список пользователей с пагинацией.

    По умолчанию возвращает первые 50 пользователей.
    """
    return map(
        mappers.user__map_to_pydantic,
        await users.read_all(
            ReadAllUsersDto(page=page, page_size=page_size), actor=actor
        ),
    )


@router.get(
    "/{user_id}",
    response_model=dtos.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def read_user_by_id(
    user_id: int,
    users: FromDishka[UsersService],
    actor: Annotated[User, Depends(get_user)],
):
    """Получает данные пользователя по его ID."""

    return mappers.user__map_to_pydantic(await users.read(user_id, actor=actor))


@router.put(
    "/{user_id}",
    response_model=dtos.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def update_user_by_id(
    user_id: int,
    dto: dtos.UpdateUserModelDto,
    users: FromDishka[UsersService],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаляет текущего пользователя."""

    return mappers.user__map_to_pydantic(
        await users.update(mappers.user__map_update_dto(dto, user_id), actor)
    )


@router.delete(
    "/{user_id}",
    response_model=dtos.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_user_by_id(
    user_id: int,
    users: FromDishka[UsersService],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаляет текущего пользователя."""

    return mappers.user__map_to_pydantic(await users.delete(user_id, actor))
