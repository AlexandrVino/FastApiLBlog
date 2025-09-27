from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.users.entities import User


class UserNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)
