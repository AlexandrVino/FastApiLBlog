from application.transactions import TransactionsGateway
from domain.posts import entities
from domain.users.entities import User

from ..auth.enums import PermissionsEnum
from ..auth.permissions import PermissionBuilder
from . import dtos
from .permissions import CategoriesPermissionProvider, PostsPermissionProvider
from .repositories import CategoriesRepository, PostsRepository


class PostsService:
    def __init__(
        self,
        repository: PostsRepository,
        tx: TransactionsGateway,
        builder: PermissionBuilder,
    ):
        self._builder = builder
        self._repository = repository
        self._transaction = tx

    async def create(self, dto: dtos.CreatePostDto, actor: User) -> entities.Post:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_CREATE_POSTS
        ).apply()

        return await self._repository.create(dto)

    async def read(self, post_id: int, actor: User) -> entities.Post:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_READ_POSTS
        ).apply()

        return await self._repository.read(post_id)

    async def read_by_category(
        self, category_id: int, actor: User
    ) -> list[entities.Post]:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_READ_ALL_POSTS
        ).apply()

        return await self._repository.read_by_category(category_id)

    async def read_all(
        self, dto: dtos.ReadAllPostsDto | None, actor: User
    ) -> list[entities.Post]:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_READ_ALL_POSTS
        ).apply()

        return await self._repository.read_all(dto)

    async def update(self, dto: dtos.UpdatePostDto, actor: User) -> entities.Post:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_UPDATE_POSTS
        ).apply()

        async with self._transaction:
            post = await self.read(dto.id, actor=actor)
            post.title = dto.title
            post.body = dto.body
            post.category_id = dto.category_id

            return await self._repository.update(post)

    async def delete(self, post_id: int, actor: User) -> entities.Post:
        self._builder.providers(PostsPermissionProvider(actor=actor, entity=None)).add(
            PermissionsEnum.CAN_DELETE_POSTS
        ).apply()

        async with self._transaction:
            post = await self.read(post_id, actor=actor)
            return await self._repository.delete(post)


class CategoriesService:
    def __init__(
        self,
        repository: CategoriesRepository,
        tx: TransactionsGateway,
        builder: PermissionBuilder,
    ):
        self._builder = builder
        self._repository = repository
        self._transaction = tx

    async def create(
        self, dto: dtos.CreateCategoryDto, actor: User
    ) -> entities.Category:
        self._builder.providers(
            CategoriesPermissionProvider(actor=actor, entity=None)
        ).add(PermissionsEnum.CAN_CREATE_CATEGORIES).apply()

        return await self._repository.create(dto)

    async def read(self, category_id: int, actor: User) -> entities.Category:
        self._builder.providers(
            CategoriesPermissionProvider(actor=actor, entity=None)
        ).add(PermissionsEnum.CAN_READ_CATEGORIES).apply()

        return await self._repository.read(category_id)

    async def read_all(
        self, dto: dtos.ReadAllCategoriesDto | None, actor: User
    ) -> list[entities.Category]:
        self._builder.providers(
            CategoriesPermissionProvider(actor=actor, entity=None)
        ).add(PermissionsEnum.CAN_READ_ALL_CATEGORIES).apply()

        return await self._repository.read_all(dto)

    async def update(
        self, dto: dtos.UpdateCategoryDto, actor: User
    ) -> entities.Category:
        self._builder.providers(
            CategoriesPermissionProvider(actor=actor, entity=None)
        ).add(PermissionsEnum.CAN_UPDATE_CATEGORIES).apply()

        async with self._transaction:
            category = await self.read(dto.id, actor=actor)
            category.title = dto.title
            category.description = dto.description

            return await self._repository.update(category)

    async def delete(self, category_id: int, actor: User) -> entities.Category:
        self._builder.providers(
            CategoriesPermissionProvider(actor=actor, entity=None)
        ).add(PermissionsEnum.CAN_DELETE_CATEGORIES).apply()

        async with self._transaction:
            category = await self.read(category_id, actor=actor)
            return await self._repository.delete(category)
