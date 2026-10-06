from fastapi import APIRouter

from app.api.v1.routers import auth, parking_places

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(parking_places.router)


__all__ = ["router"]
