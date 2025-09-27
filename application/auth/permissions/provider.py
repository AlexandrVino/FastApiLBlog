from abc import ABCMeta, abstractmethod

from domain.exceptions import Entity
from domain.users.entities import User
from domain.users.enums import RoleEnum

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


class RolePermissionProvider(PermissionProvider):
    """Провайдер прав доступа на основе роли пользователя."""

    _perms: dict[RoleEnum, set[PermissionsEnum]] = dict()

    def _get_perms(self, actor: User, entity=None) -> set[PermissionsEnum]:
        """Возвращает набор разрешений для текущего контекста."""

        result = self._perms.get(RoleEnum.USER).copy()
        if actor.role == RoleEnum.ADMIN:
            result |= self._perms.get(RoleEnum.ADMIN)

        return result
