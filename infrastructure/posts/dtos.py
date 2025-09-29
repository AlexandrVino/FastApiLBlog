from infrastructure.models import CamelModel


class CreateCategoryDto(CamelModel):
    title: str
    description: str


class ReadAllCategoriesDto(CamelModel):
    page: int
    page_size: int


class UpdateCategoryDto(CamelModel):
    title: str
    description: str


class CategoryModel(CamelModel):
    id: int
    title: str
    description: str


class CreatePostDto(CamelModel):
    body: str
    title: str
    category_id: int


class ReadAllPostsDto(CamelModel):
    page: int
    page_size: int


class UpdatePostDto(CamelModel):
    body: str
    title: str
    category_id: int


class PostModel(CamelModel):
    id: int
    body: str
    title: str


class PostModelDetail(CamelModel):
    id: int
    body: str
    title: str
    category: CategoryModel
