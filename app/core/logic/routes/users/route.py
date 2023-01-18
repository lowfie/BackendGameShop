from fastapi import APIRouter

from app.core.logic.routes.auth.route import fastapi_users
from app.core.schemas.auth_shm import UserRead, UserUpdate


users = APIRouter()

users.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

