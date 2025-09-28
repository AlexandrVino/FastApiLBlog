from dataclasses import dataclass


@dataclass
class CreatePostDto:
    body: str
    title: str
    category_id: int


@dataclass
class ReadAllPostsDto:
    page: int
    page_size: int


@dataclass
class UpdatePostDto:
    id: int
    body: str
    title: str
    category_id: int


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
