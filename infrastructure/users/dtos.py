from datetime import datetime

from domain.users.enums import RoleEnum
from infrastructure.models import CamelModel


class UpdateUserModelDto(CamelModel):
    role: RoleEnum


class UserModel(CamelModel):
    """
    Модель пользователя для API.
    """

    id: int
    email: str
    is_active: bool

    created_at: datetime
    role: RoleEnum
