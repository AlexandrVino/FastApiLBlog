from domain.users.entities import User

from ..users.dtos import CreateUserDto
from ..users.exceptions import UserNotFoundError
from ..users.services import UsersService
from .dtos import AuthenticateUserDto, RegisterUserDto
from .exceptions import InvalidCredentialsError
from .tokens.dtos import PasswordDto, TokenInfoDto, TokenPairDto
from .tokens.gateways import SecurityGateway, TokensGateway


class AuthService:
    def __init__(
        self,
        security_gateway: SecurityGateway,
        tokens_gateway: TokensGateway,
        users_service: UsersService,
    ):
        self._security_gateway = security_gateway
        self._tokens_gateway = tokens_gateway
        self._users_service = users_service

    async def authorize(self, dto: TokenInfoDto) -> User:
        try:
            user = await self._users_service.read_by_email(dto.subject)
            return user
        except UserNotFoundError:
            raise InvalidCredentialsError("email")

    async def register(self, dto: RegisterUserDto) -> tuple[User, TokenPairDto]:
        user = await self._create_user(dto)
        # TODO: add email confirmation: and remove returning user
        return user, await self._create_token_pair(user)

    async def _create_user(self, dto: RegisterUserDto):
        password_dto = self._security_gateway.create_hashed_password(dto.password)
        return await self._users_service.create(
            CreateUserDto(
                email=dto.email,
                salt=password_dto.salt,
                hashed_password=password_dto.hashed_password,
                role=dto.role,
            )
        )

    async def login(
        self, dto: AuthenticateUserDto | TokenInfoDto
    ) -> tuple[User, TokenPairDto]:
        if isinstance(dto, AuthenticateUserDto):
            return await self._login_by_password(dto)
        if isinstance(dto, TokenInfoDto):
            return await self._login_by_token(dto)
        raise ValueError(
            f'expected type "AuthenticateUserDto" | "TokenInfoDto", actual: {type(dto)}'
        )

    async def _login_by_token(self, dto: TokenInfoDto) -> tuple[User, TokenPairDto]:
        try:
            user = await self._users_service.read_by_email(dto.subject)
            return user, await self._create_token_pair(user)
        except UserNotFoundError:
            raise InvalidCredentialsError("email")

    async def _login_by_password(
        self, dto: AuthenticateUserDto
    ) -> tuple[User, TokenPairDto]:
        try:
            user = await self._users_service.read_by_email(dto.email)
            is_password_valid = self._security_gateway.verify_passwords(
                dto.password,
                PasswordDto(hashed_password=user.hashed_password, salt=user.salt),
            )
            if not is_password_valid:
                raise InvalidCredentialsError("password")
            return user, await self._create_token_pair(user)
        except UserNotFoundError:
            raise InvalidCredentialsError("email")

    async def _create_token_pair(self, user: User) -> TokenPairDto:
        return await self._tokens_gateway.create_token_pair(user.email)
