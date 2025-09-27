from typing import Any, Callable, Coroutine, Type

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from application.auth.exceptions import InvalidCredentialsError
from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidEntityPeriodError,
)


async def entity_not_found_exception_handler(_: Request, exc: EntityNotFoundError):
    """
    Обрабатывает ошибки отсутствия сущности (404 Not Found).
    """

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


async def entity_already_exists_exception_handler(
    _: Request, exc: EntityAlreadyExistsError
):
    """
    Обрабатывает ошибки дублирования сущности (400 Bad Request).
    """

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


async def entity_access_denied_handler(_: Request, exc: EntityAccessDenied):
    """
    Обрабатывает ошибки доступа к сущности (403 Forbidden).
    """

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": str(exc)},
    )


async def invalid_credentials_exception_handler(
    _: Request, exc: InvalidCredentialsError
):
    """
    Обрабатывает ошибки аутентификации (401 Unauthorized).
    """

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": str(exc)},
    )


async def invalid_entity_period_handler(_: Request, exc: InvalidEntityPeriodError):
    """
    Обрабатывает ошибки невалидного периода сущности (422 Unprocessable Entity).
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": str(exc)},
    )


def get_exception_handlers() -> list[
    tuple[Type[Exception], Callable[[Request, Any], Coroutine[Any, Any, JSONResponse]]]
]:
    return [
        (EntityNotFoundError, entity_not_found_exception_handler),
        (EntityAlreadyExistsError, entity_already_exists_exception_handler),
        (EntityAccessDenied, entity_access_denied_handler),
        (InvalidCredentialsError, invalid_credentials_exception_handler),
        (InvalidEntityPeriodError, invalid_entity_period_handler),
    ]
