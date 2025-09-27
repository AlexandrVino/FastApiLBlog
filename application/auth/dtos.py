from dataclasses import dataclass

from domain.users.enums import RoleEnum


@dataclass
class AuthenticateUserDto:
    email: str
    password: str


@dataclass
class RegisterUserDto:
    email: str
    password: str
    is_active: bool = True
    role: RoleEnum = RoleEnum.USER
