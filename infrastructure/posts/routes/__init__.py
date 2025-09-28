from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .admin_categories import router as admin_categories_router
from .admin_posts import router as admin_posts_router
from .categories import router as categories_router
from .posts import router as posts_router

router = APIRouter(route_class=DishkaRoute)
router.include_router(categories_router, prefix="/categories", tags=["Categories"])
router.include_router(posts_router, prefix="/posts", tags=["Posts"])
router.include_router(admin_posts_router, prefix="/admin/posts", tags=["Admin-Posts"])
router.include_router(
    admin_categories_router, prefix="/admin/categories", tags=["Admin-Categories"]
)
