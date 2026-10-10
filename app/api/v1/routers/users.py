from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.security import get_current_user
from app.models import User
from app.schemas.users import UserResponse

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
