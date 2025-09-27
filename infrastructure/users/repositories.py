from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.users import dtos
from application.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from application.users.repositories import UsersRepository
from domain.users import entities
from infrastructure.config import Config
from infrastructure.repositories import PostgresRepository, PostgresRepositoryConfig

from .mappers import user__create_mapper, user__map_from_db, user__map_to_db
from .models import UserDatabaseModel


class UsersDatabaseRepository(UsersRepository):
    """Репозиторий для работы с пользователями в базе данных."""

    class RepositoryConfig(PostgresRepositoryConfig):
        """Конфигурация репозитория пользователей."""

        def __init__(self):
            """Инициализирует конфигурацию маппинга пользователей."""

            super().__init__(
                model=UserDatabaseModel,
                entity=entities.User,
                entity_mapper=user__map_from_db,
                model_mapper=user__map_to_db,
                create_model_mapper=user__create_mapper,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

        def get_select_by_email_query(self, email: str) -> Select:
            """Формирует запрос для поиска пользователя по email."""

            return select(self.model).where(self.model.email == email)

        def get_select_all_query(self, dto: dtos.ReadAllUsersDto) -> Select:
            """Формирует запрос для постраничного чтения пользователей."""

            return (
                select(self.model)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession, config: Config):
        """Инициализирует репозиторий пользователей."""

        self._config = self.RepositoryConfig()
        self._admin_username = config.admin_username

        self._repository = PostgresRepository(session, self._config)

    # region queries
    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]:
        """Возвращает список пользователей с пагинацией."""

        return await self._repository.read_all(dto)

    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        """Возвращает пользователей по списку идентификаторов."""

        return await self._repository.read_by_ids(user_ids)

    async def read(self, user_id: int) -> entities.User:
        """Возвращает пользователя по идентификатору."""

        return await self._repository.read(user_id)

    async def read_by_email(self, email: str) -> entities.User:
        """Возвращает пользователя по email."""

        if model := await self._repository.get_scalar_or_none(
            self._config.get_select_by_email_query(email)
        ):
            return self._config.model_mapper(model)
        raise self._config.not_found_exception

    async def get_super_user(self) -> entities.User:
        """Возвращает суперпользователя системы."""

        return await self.read_by_email(self._admin_username)

    # endregion
    # region command
    async def create(self, dto: dtos.CreateUserDto) -> entities.User:
        """Создает нового пользователя с паролем."""

        return await self._repository.create(self._config.create_model_mapper(dto))

    async def update(self, user: entities.User) -> entities.User:
        """Обновляет данные пользователя."""

        return await self._repository.update(user)

    async def delete(self, user: entities.User) -> entities.User:
        """Удаляет пользователя."""

        return await self._repository.delete(user)

    async def _change_user_active_status(self, user_id: int, is_active: bool):
        """Изменяет статус активности пользователя."""

        query = (
            update(self._config.model)
            .where(self._config.model.id == user_id)  # noqa
            .values(is_active=is_active)
            .execution_options(synchronize_session="fetch")
            .returning(self._config.model)
        )
        await self._repository.update_by_query(query)

    # endregion
