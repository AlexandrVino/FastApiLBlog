from dishka import Provider, Scope, provide

from application.auth.tokens.gateways import SecurityGateway, TokensGateway
from infrastructure.auth.bcrypt import BcryptSecurityGateway
from infrastructure.auth.jwt import JwtTokensGateway


class GatewaysProvider(Provider):
    """Провайдер зависимостей для всех шлюзов приложения."""

    scope = Scope.APP

    tokens_gateway = provide(source=JwtTokensGateway, provides=TokensGateway)
    security_gateway = provide(source=BcryptSecurityGateway, provides=SecurityGateway)
