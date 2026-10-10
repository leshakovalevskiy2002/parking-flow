from fastapi import APIRouter

from app.api.v1.routers import auth, parking_places, parking_sessions, rates, users

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(parking_places.router)
router.include_router(rates.router)
router.include_router(parking_sessions.router)
router.include_router(users.router)


__all__ = ["router"]
