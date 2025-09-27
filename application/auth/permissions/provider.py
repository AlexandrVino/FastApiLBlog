from abc import ABCMeta, abstractmethod

from domain.users.entities import User
from domain.exceptions import Entity

from ..enums import PermissionsEnum


class PermissionProvider(metaclass=ABCMeta):
    def __init__(self, actor: User, entity: Entity):
        """
        Инициализирует провайдер с учетом активного пользователя и "страдающей" сущности
        т.е. той, в чью сторону выполняется действие
        """

        self._permissions = self._get_perms(actor, entity)

    def __call__(self) -> set[PermissionsEnum]:
        return self._permissions

    @abstractmethod
    def _get_perms(self, actor: User, entity: Entity) -> set[PermissionsEnum]: ...
