from pydantic import EmailStr

from ..models import CamelModel
from ..users.dtos import UserModel


class CreateUserModelDto(CamelModel):
    """
    Модель данных для создания нового пользователя.
    """

    email: EmailStr
    password: str


class AuthenticateUserModelDto(CamelModel):
    """
    Модель данных для аутентификации пользователя.
    """

    email: EmailStr
    password: str


class UserWithTokenModel(CamelModel):
    """Модель ответа API, содержащая данные пользователя и его access-токен.

    Используется для возврата данных после успешной аутентификации или регистрации.
    """

    access_token: str
    user: UserModel
