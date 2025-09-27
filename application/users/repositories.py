from abc import ABCMeta, abstractmethod

from domain.users import entities

from . import dtos


class UsersRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateUserDto) -> entities.User: ...

    @abstractmethod
    async def read(self, user_id: int) -> entities.User: ...

    @abstractmethod
    async def read_by_email(self, email: str) -> entities.User: ...

    @abstractmethod
    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]: ...

    @abstractmethod
    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]: ...

    @abstractmethod
    async def update(self, user: entities.User) -> entities.User: ...

    @abstractmethod
    async def delete(self, user: entities.User) -> entities.User: ...

    @abstractmethod
    async def _change_user_active_status(
        self, user_id: int, is_active: bool
    ) -> entities.User: ...
