from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.core.database.models import User
from app.core.logic.routes.auth.auth_backend import auth_backend
from app.core.logic.routes.auth.user_manager import get_user_manager
from app.core.schemas.auth_shm import UserRead, RegisterIn, UserUpdate

from app.core.logic.routes.users.route import users

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_route = APIRouter()

auth_route.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_route.include_router(
    fastapi_users.get_register_router(UserRead, RegisterIn),
    prefix="/auth",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
