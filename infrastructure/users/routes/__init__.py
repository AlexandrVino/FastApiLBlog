from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .admin import router as admin_router
from .users import router as users_router

router = APIRouter(route_class=DishkaRoute, tags=["Users"])
router.include_router(users_router)
router.include_router(admin_router, prefix="/admin")
