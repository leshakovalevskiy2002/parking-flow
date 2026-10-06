from fastapi import APIRouter

from app.api.v1.routers import auth

router = APIRouter(prefix="/v1")

router.include_router(auth.router)


__all__ = ["router"]
