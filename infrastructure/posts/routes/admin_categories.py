from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from application.posts.services import CategoriesService
from domain.users.entities import User
from infrastructure.auth.deps import get_user
from infrastructure.posts import dtos, mappers

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=dtos.CategoryModel)
async def create_category(
    dto: dtos.CreateCategoryDto,
    actor: Annotated[User, Depends(get_user)],
    categories: FromDishka[CategoriesService],
):
    return mappers.category__map_to_pydantic(
        await categories.create(mappers.category__create_dto_mapper(dto), actor)
    )


@router.put("/{category_id}", response_model=dtos.CategoryModel)
async def update_category(
    category_id: int,
    dto: dtos.UpdateCategoryDto,
    actor: Annotated[User, Depends(get_user)],
    categories: FromDishka[CategoriesService],
):
    return mappers.category__map_to_pydantic(
        await categories.update(
            mappers.category__map_update_dto(dto, category_id), actor
        )
    )


@router.delete("/{category_id}", response_model=dtos.CategoryModel)
async def delete_category(
    category_id: int,
    actor: Annotated[User, Depends(get_user)],
    categories: FromDishka[CategoriesService],
):
    return mappers.category__map_to_pydantic(
        await categories.delete(category_id, actor)
    )
