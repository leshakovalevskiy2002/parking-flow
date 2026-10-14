from fastapi import APIRouter

from app.api.v1.routers import auth, fines, parking_places, parking_sessions, rates, users
from app.api.v1.routers.admin import parking_sessions as parking_sessions_admin
from app.api.v1.routers.inspector import fines as fines_inspector

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(parking_places.router)
router.include_router(rates.router)
router.include_router(parking_sessions.router)
router.include_router(parking_sessions_admin.router)
router.include_router(users.router)
router.include_router(fines_inspector.router)
router.include_router(fines.router)


__all__ = ["router"]
