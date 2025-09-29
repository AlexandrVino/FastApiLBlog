from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.posts.entities import Category, Post


class PostNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Post)


class PostAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Post)


class CategoryNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Category)


class CategoryAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Category)
