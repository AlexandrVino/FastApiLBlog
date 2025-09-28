from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.users import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.get("/me", response_model=dtos.UserModel)
async def get_me(actor: Annotated[User, Depends(get_user)]):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.user__map_to_pydantic(actor)
