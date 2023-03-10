from fastapi import APIRouter

from app.core.logic.routes.auth.route import auth_route
from app.core.logic.routes.users.route import users
from app.core.logic.routes.games.route import games
from app.core.logic.routes.cart.route import cart
from app.core.logic.routes.economy.route import economy
from app.core.logic.routes.user_library.route import library
from app.core.logic.routes.compilation.route import compilation
from app.core.logic.routes.reviews.route import reviews


api_router = APIRouter()

api_router.include_router(auth_route)
api_router.include_router(users, tags=['users'])
api_router.include_router(games, tags=['games'])
api_router.include_router(cart, tags=['cart'])
api_router.include_router(economy, tags=['economy'])
api_router.include_router(library, tags=['user_library'])
api_router.include_router(compilation, tags=['compilation'])
api_router.include_router(reviews, tags=['reviews'])
