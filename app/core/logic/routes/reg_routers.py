from fastapi import APIRouter

from app.core.logic.routes.auth.route import auth_route
from app.core.logic.routes.users.route import users

api_router = APIRouter()

api_router.include_router(auth_route)
api_router.include_router(users, tags=['users'])
