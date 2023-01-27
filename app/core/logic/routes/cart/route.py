from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse

from app.core.schemas.cart_shm import GetMyCart
from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import Cart, User, Game, UserBalance, UserGames
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, func, update


cart = APIRouter()
current_user = fastapi_users.current_user()


@cart.post('/add_to_cart/')
async def add_game_to_cart(game: int, user: User = Depends(current_user),
                           session: AsyncSession = Depends(get_session)):
    permissions = (await session.execute(
        select(Game.id.label('is_exists'),
               Cart.game_id.label('is_game_added'),
               UserGames.game_id.label('is_library'))
        .outerjoin(Cart)
        .outerjoin(UserGames)
        .where(Game.id.__eq__(game))
    )).first()

    if permissions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='GAME_NOT_FOUND')
    elif permissions['is_game_added']:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='GAME_ALREADY_ADDED')
    elif permissions['is_library']:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='GAME_ALREADY_PURCHASED')

    await session.execute(
        insert(Cart).values(
            user_id=user.id,
            game_id=game
        )
    )
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'GAME_SUCCESSFULLY_ADDED'})


@cart.get('/my_cart/', response_model=GetMyCart)
async def get_cart(user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_session)):
    user_games_cart = (await session.execute(
        select(Game.id, Game.title, Game.description, Game.image_path)
        .join(Cart)
        .where(Cart.user_id.__eq__(user.id))
    )).all()
    user_games_cart = [dict(item) for item in user_games_cart]
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': user_games_cart})


@cart.delete('/clear_cart/')
async def delete_all_games_cart(user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_session)):
    game_cart_ids = (await (session.execute(
        select(Cart.game_id)
        .where(User.id.__eq__(user.id))))).all()
    game_cart_ids = [id_['game_id'] for id_ in game_cart_ids]
    await session.execute(delete(Cart).where(Cart.game_id.in_(game_cart_ids)))
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'CART_WAS_CLEARED'})


@cart.delete('/delete_game_cart/')
async def delete_game_byid_cart(games: list[int] = Query(), user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Cart).where(Cart.game_id.in_(games)))
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'GAMES_WAS_DELETED'})


@cart.patch('/buy_cart/')
async def buy_all_products_cart(user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_session)):
    remains = (await session.execute(
        select(UserBalance.balance - func.sum(Game.price))
        .where(UserBalance.user_id.__eq__(user.id))
        .select_from(Cart)
        .join(Game)
        .group_by(UserBalance)
    )).scalar()

    if remains < 0:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail={'result': 'INSUFFICIENT_FUNDS'})

    await session.execute(update(UserBalance).values(balance=remains).where(UserBalance.user_id.__eq__(user.id)))
    buy_games = (await session.execute(select(Cart.game_id).where(Cart.user_id.__eq__(user.id)))).all()
    await session.execute(delete(Cart).where(Cart.user_id.__eq__(user.id)))
    for game in buy_games:
        await session.execute(insert(UserGames).values(user_id=user.id, game_id=game['game_id']))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'PURCHASE_IS_SUCCESSFUL'})


@cart.put('/buy_games_cart/')
async def buy_products_cart(games: list[int] = Query(), user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_session)):
    remains = (await session.execute(
        select(UserBalance.balance - func.sum(Game.price))
        .where(
            UserBalance.user_id.__eq__(user.id),
            Cart.game_id.in_(games)
        )
        .select_from(Cart)
        .join(Game)
        .group_by(UserBalance)
    )).scalar()

    if remains < 0:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail={'result': 'INSUFFICIENT_FUNDS'})

    await session.execute(update(UserBalance).values(balance=remains).where(UserBalance.user_id.__eq__(user.id)))
    buy_games = (await session.execute(select(Cart.game_id).where(Cart.user_id.__eq__(user.id)))).all()
    await session.execute(delete(Cart).where(Cart.game_id.in_(games)))
    for game in buy_games:
        await session.execute(insert(UserGames).values(user_id=user.id, game_id=game['game_id']))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'PURCHASE_IS_SUCCESSFUL'})


