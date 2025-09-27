from application.transactions import TransactionsGateway
from domain.users.entities import User

from ..auth.enums import PermissionsEnum
from ..auth.permissions import PermissionBuilder
from .dtos import CreateUserDto, ReadAllUsersDto, UpdateUserDto
from .permissions import UsersPermissionProvider
from .repositories import UsersRepository


class UsersService:
    def __init__(
        self,
        repository: UsersRepository,
        tx: TransactionsGateway,
        builder: PermissionBuilder,
    ):
        self._builder = builder
        self._repository = repository
        self._transaction = tx

    async def create(self, dto: CreateUserDto) -> User:
        return await self._repository.create(dto)

    async def read(self, user_id: int, actor: User) -> User:
        user = await self._repository.read(user_id)
        self._builder.providers(UsersPermissionProvider(actor=actor, entity=user)).add(
            PermissionsEnum.CAN_READ_USERS
        ).apply()
        return user

    async def read_all(self, dto: ReadAllUsersDto, actor: User) -> list[User]:
        users = await self._repository.read_all(dto)
        self._builder.providers(UsersPermissionProvider(actor=actor, entity=users)).add(
            PermissionsEnum.CAN_READ_ALL_USERS
        ).apply()
        return await self._repository.read_all(dto)

    async def read_by_email(self, email: str) -> User:
        return await self._repository.read_by_email(email)

    async def read_by_ids(self, user_ids: list[int], actor: User) -> list[User]:
        users = await self._repository.read_by_ids(user_ids)
        self._builder.providers(UsersPermissionProvider(actor=actor, entity=users)).add(
            PermissionsEnum.CAN_READ_ALL_USERS
        ).apply()
        return users

    async def update(self, dto: UpdateUserDto, actor: User) -> User:
        async with self._transaction:
            user = await self.read(dto.user_id, actor=actor)
            self._builder.providers(
                UsersPermissionProvider(actor=actor, entity=user)
            ).add(PermissionsEnum.CAN_UPDATE_USERS).apply()
            user.role = dto.role

            return await self._repository.update(user)

    async def delete(self, user_id: int, actor: User) -> User:
        async with self._transaction:
            user = await self.read(user_id, actor=actor)
            self._builder.providers(
                UsersPermissionProvider(actor=actor, entity=user)
            ).add(PermissionsEnum.CAN_DELETE_USERS).apply()

            return await self._repository.delete(user)
