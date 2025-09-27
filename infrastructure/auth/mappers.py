from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function

from application.auth.dtos import AuthenticateUserDto, RegisterUserDto

from ..mappers import pydantic_retort
from .dtos import AuthenticateUserModelDto, CreateUserModelDto

retort = pydantic_retort.extend(recipe=[])

map_authenticate_dto = retort.get_converter(
    AuthenticateUserModelDto,
    AuthenticateUserDto,
    recipe=[
        link_function(
            lambda user: user.email,
            P[AuthenticateUserDto].email,
        ),
    ],
)

map_create_dto = retort.get_converter(
    CreateUserModelDto,
    RegisterUserDto,
    recipe=[
        link_function(
            lambda user: user.email,
            P[RegisterUserDto].email,
        ),
        allow_unlinked_optional(P[RegisterUserDto].is_active),
        allow_unlinked_optional(P[RegisterUserDto].role),
    ],
)
