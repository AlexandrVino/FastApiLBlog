from dishka import Provider, Scope, provide

from application.posts.repositories import CategoriesRepository, PostsRepository
from application.users.repositories import UsersRepository
from infrastructure.posts.repositories import (
    CategoriesDatabaseRepository,
    PostsDatabaseRepository,
)
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
    posts_repository = provide(source=PostsDatabaseRepository, provides=PostsRepository)
    categories_repository = provide(
        source=CategoriesDatabaseRepository, provides=CategoriesRepository
    )
