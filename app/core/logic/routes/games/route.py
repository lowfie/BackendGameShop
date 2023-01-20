from fastapi import APIRouter, Depends, HTTPException, status

from app.core.logic.routes.auth.route import fastapi_users
from app.core.schemas.games_shm import CreateGameOut, UpdateGame
from app.core.database.models import Game, User
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete


games = APIRouter()
current_user = fastapi_users.current_user()


@games.post('/add_game/', response_model=CreateGameOut)
async def add_game(game: CreateGameOut, user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_session)):
    is_game = (await session.execute(select(Game.title).where(Game.title.__eq__(game.title)))).first()
    if is_game:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail='GAME_ALREADY_EXISTS'
        )

    await session.execute(
        insert(Game).values(
            title=game.title,
            description=game.description,
            price=game.price,
            discount=game.discount,
            image_path=game.image_path,
            start_date=game.start_date,
            user_id=user.id
        )
    )
    await session.commit()
    return game


@games.patch('/update_game/', response_model=UpdateGame)
async def update_game_by_id(game: UpdateGame, game_id: int, user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_session)):
    user_games = (await session.execute(
        select(Game.id)
        .join(User)
        .where(Game.user_id.__eq__(user.id))
    )).all()
    user_games = [item['id'] for item in user_games]

    if game_id not in user_games:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"THIS_NOT_YOUR_GAME")

    await session.execute(
        update(Game)
        .values(title=game.title,
                description=game.description,
                price=game.price,
                discount=game.discount
                )
        .where(Game.id.__eq__(game_id))
    )
    await session.commit()
    return game


@games.get('/get_my_games/')
async def get_all_user_games(user: User = Depends(current_user),
                             session: AsyncSession = Depends(get_session)):
    user_games = (await session.execute(
        select(Game.id, Game.title, Game.price)
        .join(User)
        .where(Game.user_id.__eq__(user.id))
    )).all()
    return user_games


@games.get('/get_game_by_id/')
async def get_game_by_id(game_id: int, user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_session)):
    game_by_id = (await session.execute(
        select(Game.id,
               Game.title,
               Game.description,
               Game.price,
               Game.discount,
               Game.image_path,
               Game.start_date
               )
        .where(Game.id.__eq__(game_id))
    )).first()

    if not game_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='GAME_NOT_FOUND')

    return game_by_id


@games.delete('/delete_my_game/')
async def delete_user_game(game_id: int, user: User = Depends(current_user),
                           session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Game).where(Game.id.__eq__(game_id)))
    await session.commit()
    return {"result": "GAME_WAS_DELETED"}

