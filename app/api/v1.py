from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.item.router import router as item_router

router = APIRouter(
    prefix="/api/v1",
)


router.include_router(auth_router)
router.include_router(item_router)
