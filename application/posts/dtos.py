from dataclasses import dataclass

from domain.posts.entities import Category
from domain.users.enums import RoleEnum


@dataclass
class CreatePostDto:
    body: str
    title: str
    category: Category


@dataclass
class ReadAllPostsDto:
    page: int
    page_size: int


@dataclass
class UpdatePostDto:
    id: int
    body: str
    title: str
    category: Category


@dataclass
class CreateCategoryDto:
    title: str
    description: str


@dataclass
class ReadAllCategoriesDto:
    page: int
    page_size: int


@dataclass
class UpdateCategoryDto:
    id: int
    title: str
    description: str
