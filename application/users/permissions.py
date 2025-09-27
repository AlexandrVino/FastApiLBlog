from domain.users.entities import User
from domain.users.enums import RoleEnum
from ..auth.enums import PermissionsEnum
from ..auth.permissions import PermissionProvider


class UsersPermissionProvider(PermissionProvider):
    """Провайдер прав доступа для работы с пользователями.

    Определяет набор разрешений для различных ролей пользователей
    с учетом видимости связанного события.
    """

    _perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.ADMIN: {
            PermissionsEnum.CAN_CREATE_USERS,
            PermissionsEnum.CAN_READ_USERS,
            PermissionsEnum.CAN_READ_ALL_USERS,
            PermissionsEnum.CAN_UPDATE_USERS,
            PermissionsEnum.CAN_DELETE_USERS,
        },
        RoleEnum.USER: {
            PermissionsEnum.CAN_CREATE_USERS,
            PermissionsEnum.CAN_READ_USERS,
            PermissionsEnum.CAN_DELETE_USERS,
        },
        RoleEnum.PUBLIC: {PermissionsEnum.CAN_CREATE_USERS},
    }

    def _get_perms(
        self,
        actor: User,
        entity: None | User | list[User],
    ) -> set[PermissionsEnum]:
        """Возвращает набор разрешений для текущего контекста."""

        result = self._perms.get(RoleEnum.PUBLIC).copy()
        if actor.role == RoleEnum.ADMIN:
            result |= self._perms.get(RoleEnum.ADMIN)
        if isinstance(entity, User) and actor.id == entity.id:
            result |= self._perms.get(RoleEnum.USER)

        return result
