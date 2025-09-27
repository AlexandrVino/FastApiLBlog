from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .auth import router as auth_router
from .posts import router as post_router
from .users import router as user_router

v1_router = APIRouter(route_class=DishkaRoute, prefix="/v1")

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(user_router, prefix="/users")
v1_router.include_router(post_router)
