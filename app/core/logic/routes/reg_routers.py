from fastapi import APIRouter

from app.core.logic.routes.auth.route import auth_route
from app.core.logic.routes.users.route import users
from app.core.logic.routes.games.route import games
from app.core.logic.routes.cart.route import cart

api_router = APIRouter()

api_router.include_router(auth_route)
api_router.include_router(users, tags=['users'])
api_router.include_router(games, tags=['games'])
api_router.include_router(cart, tags=['cart'])
