import asyncio

from dishka import AsyncContainer

from application.auth.services import AuthService, RegisterUserDto
from application.users.exceptions import UserNotFoundError
from application.users.repositories import UsersRepository
from domain.users.entities import User
from domain.users.enums import RoleEnum
from infrastructure.config import Config
from infrastructure.providers.container import create_container


async def _create_admin(
    config: Config,
    users_repository: UsersRepository,
    auth: AuthService,
):
    dto = RegisterUserDto(
        email=config.admin_username,
        password=config.admin_password,
        role=RoleEnum.ADMIN,
    )
    try:
        return await users_repository.read_by_email(dto.email)
    except UserNotFoundError:
        return await auth._create_user(dto)  # noqa


async def init(container: AsyncContainer):
    async with container() as nested:
        config = await nested.get(Config)
        auth = await nested.get(AuthService)

        users_repository = await nested.get(UsersRepository)
        admin = await _create_admin(config, users_repository, auth)


if __name__ == "__main__":
    asyncio.run(init(create_container()))
