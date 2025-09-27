from typing import TypeVar

Entity = TypeVar("Entity")


class EntityException(Exception):
    """
    Стандартная ошибка от которой все ошибки наследуются
    """

    pass


class EntityNotFoundError(EntityException):
    """
    Стандартная ошибка NotFound от которой все ошибки NotFound наследуются
    """

    def __init__(self, entity: type[Entity] | None = None, **kwargs):
        super().__init__(f"{entity.__name__} not found ({kwargs})")


class EntityAlreadyExistsError(EntityException):
    """
    Стандартная ошибка AlreadyExists от которой все ошибки AlreadyExists наследуются
    """

    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"{entity.__name__} already exists")


class EntityAccessDenied(EntityException):
    """
    Стандартная ошибка AccessDenied от которой все ошибки AccessDenied наследуются
    """

    def __init__(self):
        super().__init__("Access denied")


class InvalidEntityPeriodError(EntityException):
    """
    Стандартная ошибка InvalidEntityPeriodError от которой все ошибки InvalidEntityPeriodError наследуются
    """

    def __init__(self, entity: type[Entity] | None = None):
        super().__init__(f"Invalid {entity.__name__} period")
