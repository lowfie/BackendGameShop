from fastapi import APIRouter

from app.core.logic.routes.auth.route import auth_route

api_router = APIRouter()

api_router.include_router(auth_route)

