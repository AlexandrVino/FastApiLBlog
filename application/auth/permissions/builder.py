from domain.exceptions import EntityAccessDenied

from ..enums import PermissionsEnum
from ..permissions.provider import PermissionProvider


class PermissionBuilder:
    def __init__(self):
        self._permissions = set()
        self._necessary = set()

    def providers(self, *providers: PermissionProvider) -> "PermissionBuilder":
        for provider in providers:
            self._permissions |= provider()
        return self

    def add(self, *args: PermissionsEnum) -> "PermissionBuilder":
        self._necessary |= set(args)
        return self

    def apply(self):
        if not self._necessary <= self._permissions:
            raise EntityAccessDenied()
