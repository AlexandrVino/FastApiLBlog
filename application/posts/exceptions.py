from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.users.entities import User


class PostNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)


class PostAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)


class CategoryNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(User)


class CategoryAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(User)
