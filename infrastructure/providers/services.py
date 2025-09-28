from dishka import Provider, Scope, provide

from application.auth.services import AuthService
from application.posts.services import CategoriesService, PostsService
from application.users.services import UsersService


class ServiceProvider(Provider):
    """
    Провайдер для всех Use Cases (сценариев использования) приложения.

    Группирует и предоставляет все use cases по функциональным областям
    с областью видимости на уровне запроса (REQUEST).
    Каждый запрос получает новые экземпляры use cases.
    """

    scope = Scope.REQUEST

    auth = provide(AuthService)
    users = provide(UsersService)
    posts = provide(PostsService)
    categories = provide(CategoriesService)
