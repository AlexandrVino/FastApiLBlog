from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from domain.users.enums import RoleEnum
from infrastructure.postgres import Base


class UserDatabaseModel(Base):
    """
    Основная модель пользователя в базе данных.
    Содержит учетные данные, контактные данные и настройки пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    salt: Mapped[str]
    hashed_password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    role: Mapped[RoleEnum] = mapped_column(
        ENUM(RoleEnum, name="RoleEnum"), nullable=False, default=RoleEnum.USER
    )
