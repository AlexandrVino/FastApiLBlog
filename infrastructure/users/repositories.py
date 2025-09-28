from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.users import dtos
from application.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from application.users.repositories import UsersRepository
from domain.users import entities
from infrastructure.config import Config

from ..repositories.config import CRUDRepositoryConfig, MapperConfig
from ..repositories.repositories import CRUDDatabaseRepository
from . import mappers
from .models import UserDatabaseModel


class RepositoryConfig(
    CRUDRepositoryConfig[
        dtos.CreateUserDto,
        dtos.ReadAllUsersDto,
        entities.User,
        UserDatabaseModel,
        UserNotFoundError,
        UserAlreadyExistsError,
    ]
):
    def get_select_by_email_query(self, email: str) -> Select:
        """Формирует запрос для поиска пользователя по email."""
        return select(self.model).where(self.model.email == email)


class UsersDatabaseRepository(
    CRUDDatabaseRepository[
        dtos.CreateUserDto,
        dtos.ReadAllUsersDto,
        entities.User,
        UserDatabaseModel,
        UserNotFoundError,
        UserAlreadyExistsError,
    ],
    UsersRepository,
):
    """Репозиторий для работы с пользователями в базе данных."""

    _config = RepositoryConfig(
        read_all_dto=dtos.CreateUserDto,
        model=UserDatabaseModel,
        entity=entities.User,
        create_mapper=mappers.user__create_mapper,
        entity_mapper=mappers.user__map_from_db,
        model_mapper=mappers.user__map_to_db,
        not_found_exception=UserNotFoundError,
        already_exists_exception=UserAlreadyExistsError,
    )

    def __init__(self, session: AsyncSession, config: Config):
        """Инициализирует репозиторий пользователей."""

        super().__init__(session)
        self._admin_username = config.admin_username

    # region queries
    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        """Возвращает пользователей по списку идентификаторов."""

        return await self._repository.read_by_ids(user_ids)

    async def read_by_email(self, email: str) -> entities.User:
        """Возвращает пользователя по email."""

        if model := await self._repository.get_scalar_or_none(
            self._config.get_select_by_email_query(email)
        ):
            return self._config.entity_mapper(model)
        raise self._config.not_found_exception

    async def get_super_user(self) -> entities.User:
        """Возвращает суперпользователя системы."""

        return await self.read_by_email(self._admin_username)

    # endregion
