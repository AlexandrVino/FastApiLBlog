from dishka import Provider, Scope, provide

from application.auth.permissions import PermissionBuilder


class PermissionProvider(Provider):
    """
    Провайдер зависимостей для системы управления разрешениями.

    Предоставляет компоненты для построения и проверки прав доступа
    с областью видимости на уровне запроса (REQUEST).
    """

    scope = Scope.REQUEST

    builder = provide(source=PermissionBuilder)
