from domain.users.enums import RoleEnum

from ..auth.enums import PermissionsEnum
from ..auth.permissions import RolePermissionProvider


class PostsPermissionProvider(RolePermissionProvider):
    """Провайдер прав доступа для работы с постами."""

    _perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.ADMIN: {
            PermissionsEnum.CAN_CREATE_POSTS,
            PermissionsEnum.CAN_READ_POSTS,
            PermissionsEnum.CAN_UPDATE_POSTS,
            PermissionsEnum.CAN_DELETE_POSTS,
            PermissionsEnum.CAN_READ_ALL_POSTS,
        },
        RoleEnum.USER: {
            PermissionsEnum.CAN_READ_POSTS,
            PermissionsEnum.CAN_READ_ALL_POSTS,
        },
        RoleEnum.PUBLIC: {
            PermissionsEnum.CAN_READ_POSTS,
            PermissionsEnum.CAN_READ_ALL_POSTS,
        },
    }


class CategoriesPermissionProvider(RolePermissionProvider):
    """Провайдер прав доступа для работы с категориями."""

    _perms: dict[RoleEnum, set[PermissionsEnum]] = {
        RoleEnum.ADMIN: {
            PermissionsEnum.CAN_CREATE_CATEGORIES,
            PermissionsEnum.CAN_READ_CATEGORIES,
            PermissionsEnum.CAN_UPDATE_CATEGORIES,
            PermissionsEnum.CAN_DELETE_CATEGORIES,
            PermissionsEnum.CAN_READ_ALL_CATEGORIES,
        },
        RoleEnum.USER: {
            PermissionsEnum.CAN_READ_CATEGORIES,
            PermissionsEnum.CAN_READ_ALL_CATEGORIES,
        },
        RoleEnum.PUBLIC: {
            PermissionsEnum.CAN_READ_CATEGORIES,
            PermissionsEnum.CAN_READ_ALL_CATEGORIES,
        },
    }
