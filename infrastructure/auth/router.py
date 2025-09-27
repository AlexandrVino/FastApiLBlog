from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from application.auth.services import AuthService
from application.auth.tokens.dtos import TokenInfoDto, TokenPairDto
from domain.users.entities import User
from infrastructure.auth.deps import extract_refresh_token
from infrastructure.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
    UserWithTokenModel,
)
from infrastructure.auth.mappers import map_authenticate_dto, map_create_dto
from infrastructure.users.mappers import user__map_to_pydantic

router = APIRouter(route_class=DishkaRoute, tags=["Auth"])
REFRESH_COOKIE = "refresh"


def _make_response(user: User, tokens_pair: TokenPairDto):
    """Формирует HTTP-ответ с данными пользователя и токенами.

    Создает JSON-ответ с моделью пользователя и access-токеном,
    а также устанавливает refresh-токен в cookies.
    """

    response = JSONResponse(
        content=UserWithTokenModel(
            user=user__map_to_pydantic(user),
            access_token=tokens_pair.access_token,
        ).model_dump(by_alias=True, mode="json"),
    )
    response.set_cookie(REFRESH_COOKIE, tokens_pair.refresh_token)
    return response


@router.post("/login", response_model=UserWithTokenModel)
async def login_user(
    auth_data: AuthenticateUserModelDto,
    auth: FromDishka[AuthService],
):
    """Эндпоинт для аутентификации пользователя.

    Принимает учетные данные и возвращает данные пользователя
    с токенами доступа при успешной аутентификации.
    """

    user, tokens_pair = await auth.login(map_authenticate_dto(auth_data))
    return _make_response(user, tokens_pair)


@router.post("/register", response_model=UserWithTokenModel)
async def register_user(
    dto: CreateUserModelDto,
    auth: FromDishka[AuthService],
):
    """Эндпоинт для регистрации нового пользователя.

    Принимает данные для регистрации и создает новую учетную запись.
    """

    user, tokens_pair = await auth.register(map_create_dto(dto))
    return _make_response(user, tokens_pair)


@router.post("/refresh", response_model=UserWithTokenModel)
async def refresh_token(
    token_info: Annotated[TokenInfoDto, Depends(extract_refresh_token)],
    auth: FromDishka[AuthService],
):
    """Эндпоинт для обновления токенов доступа.

    Генерирует новую пару токенов на основе валидного refresh-токена.
    """
    user, tokens_pair = await auth.authorize(token_info)
    return _make_response(user, tokens_pair)
