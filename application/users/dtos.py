from dataclasses import dataclass

from domain.users.enums import RoleEnum


@dataclass
class ReadAllUsersDto:
    page: int
    page_size: int


@dataclass
class UpdateUserDto:
    user_id: int
    role: RoleEnum


@dataclass
class CreateUserDto:
    email: str
    salt: str
    hashed_password: str
    role: RoleEnum
