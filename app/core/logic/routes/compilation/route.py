from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core.schemas.compilation_shm import CompilationSchemas
from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import User, Game, UserGames
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func

compilation = APIRouter()
current_user = fastapi_users.current_user()


@compilation.get('/novelties/', response_model=CompilationSchemas)
async def collection_novelties(session: AsyncSession = Depends(get_session),
                               user: User = Depends(current_user)):
    novelties_games = (await session.execute(
        select(Game.title, Game.price, Game.image_path)
        .order_by(desc(Game.start_date))
        .limit(50)
    )).all()
    novelties_games = jsonable_encoder(novelties_games)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': novelties_games})


@compilation.get('/popular/', response_model=CompilationSchemas)
async def collection_popular(session: AsyncSession = Depends(get_session),
                             user: User = Depends(current_user)):
    popular_games = (await session.execute(
        select(Game.title, Game.price, Game.image_path, func.count(UserGames.game_id))
        .join(Game)
        .group_by(Game.id, UserGames.game_id)
        .limit(50)
    )).all()
    popular_games = jsonable_encoder(popular_games)
    return JSONResponse(status_code=status.HTTP_200_OK, content=popular_games)
