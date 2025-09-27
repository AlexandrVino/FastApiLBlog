from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.users.services import UsersService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.models import ErrorModel
from infrastructure.users import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/me", response_model=dtos.UserModel)
async def get_me(actor: Annotated[User, Depends(get_user)]):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.user__map_to_pydantic(actor)


@router.delete(
    "/me", response_model=dtos.UserModel, responses={404: {"model": ErrorModel}}
)
async def delete_me(
    users: FromDishka[UsersService],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаляет текущего пользователя."""

    return mappers.user__map_to_pydantic(
        await users.delete(user_id=actor.id, actor=actor)
    )
