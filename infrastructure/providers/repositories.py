from dishka import Provider, Scope, provide

from application.users.repositories import UsersRepository
from infrastructure.users.repositories import UsersDatabaseRepository


class RepositoriesProvider(Provider):
    """
    Провайдер зависимостей для всех репозиториев приложения.

    Обеспечивает доступ к репозиториям базы данных с областью видимости
    на уровне запроса (REQUEST). Каждый репозиторий предоставляется
    как реализация соответствующего интерфейса.
    """

    scope = Scope.REQUEST
    users_repository = provide(source=UsersDatabaseRepository, provides=UsersRepository)
