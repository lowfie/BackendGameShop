from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import User, UserGames, Game
from app.core.schemas.library_shm import LibrarySchema
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

library = APIRouter()
current_user = fastapi_users.current_user()


@library.get('/my_library/', response_model=LibrarySchema)
async def get_all_purchased_games(session: AsyncSession = Depends(get_session),
                                  user: User = Depends(current_user)):
    library_games = (await session.execute(
        select(Game.title,
               Game.description,
               Game.image_path,
               Game.start_date)
        .join(UserGames)
    )).all()
    library_games = jsonable_encoder(library_games)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': library_games})
