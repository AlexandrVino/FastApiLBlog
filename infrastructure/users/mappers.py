from adaptix import P
from adaptix.conversion import allow_unlinked_optional, link_function

from application.users.dtos import CreateUserDto, UpdateUserDto
from domain.users.entities import User
from infrastructure.mappers import postgres_retort, pydantic_retort

from .dtos import UpdateUserModelDto, UserModel
from .models import UserDatabaseModel

retort = postgres_retort.extend(recipe=[])


user__map_from_db = retort.get_converter(UserDatabaseModel, User)

user__map_to_db = retort.get_converter(User, UserDatabaseModel)

user__create_mapper = retort.get_converter(
    CreateUserDto,
    UserDatabaseModel,
    recipe=[
        allow_unlinked_optional(P[UserDatabaseModel].id),
        allow_unlinked_optional(P[UserDatabaseModel].is_active),
        allow_unlinked_optional(P[UserDatabaseModel].created_at),
    ],
)

retort = pydantic_retort.extend(recipe=[])

user__map_to_pydantic = retort.get_converter(User, UserModel)


@retort.impl_converter(
    recipe=[
        link_function(
            lambda dto, user_id: user_id,
            P[UpdateUserDto].user_id,
        )
    ]
)
def user__map_update_dto(dto: UpdateUserModelDto, user_id: int) -> UpdateUserDto: ...  # noqa
