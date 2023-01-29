from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import Review, User, Game, UserGames
from app.core.schemas.reviews_shm import ReviewToChange, ReviewsUsers
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, desc, delete

import datetime

reviews = APIRouter()
current_user = fastapi_users.current_user()


@reviews.post('/create_overview/')
async def leave_review(review: ReviewToChange,
                       session: AsyncSession = Depends(get_session),
                       user: User = Depends(current_user)):
    permissions = (await session.execute(
        select(UserGames.game_id.label('is_buy'), Review.game_id.label('is_review'))
        .outerjoin(Review, Review.game_id == UserGames.game_id)
        .where(UserGames.game_id.__eq__(review.game_id))
    )).first()

    if permissions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='GAME_NOT_FOUND'
        )
    elif not permissions['is_buy']:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='GAME_IS_NOT_PURCHASED'
        )
    elif permissions['is_review']:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='REVIEW_ALREADY_LEFT_FOR_GAME'
        )

    await session.execute(
        insert(Review)
        .values(
            user_id=user.id,
            game_id=review.game_id,
            title=review.title,
            text=review.text,
            evaluation=review.evaluation,
            date_of_create=datetime.datetime.now(),
            date_of_change=None
        ))
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'REVIEW_SUCCESSFULLY_LEFT'})


@reviews.patch('/edit_review/', response_model_exclude_unset=True)
async def edit_left_review(review: ReviewToChange,
                           session: AsyncSession = Depends(get_session),
                           user: User = Depends(current_user)):
    await session.execute(
        update(Review)
        .values(
            title=review.title,
            text=review.text,
            evaluation=review.evaluation,
            date_of_change=datetime.datetime.now()
        )
        .where(Review.game_id.__eq__(review.game_id), Review.user_id.__eq__(user.id)))
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'REVIEW_SUCCESSFULLY_EDITED'})


@reviews.get('/my_reviews/', response_model=ReviewsUsers)
async def my_reviews(session: AsyncSession = Depends(get_session),
                     user: User = Depends(current_user)):
    user_reviews = (await session.execute(
        select(Review.game_id,
               Review.title,
               Review.text,
               Review.evaluation,
               Review.date_of_create,
               Review.date_of_change
               )
        .where(Review.user_id.__eq__(user.id))
        .order_by(desc(Review.date_of_create))
    )).all()
    user_reviews = jsonable_encoder(user_reviews)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': user_reviews})


@reviews.get('/latest_game_reviews/', response_model=ReviewsUsers)
async def latest_game_reviews(session: AsyncSession = Depends(get_session),
                              user: User = Depends(current_user)):
    latest_review_users = (await session.execute(
        select(Review.game_id,
               Review.title,
               Review.text,
               Review.evaluation,
               Review.date_of_create,
               Review.date_of_change
               )
        .order_by(desc(Review.date_of_create))
        .limit(50)
    )).all()
    latest_review_users = jsonable_encoder(latest_review_users)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': latest_review_users})


@reviews.delete('/delete_my_review/')
async def delete_review_by_id(game_id: int,
                              session: AsyncSession = Depends(get_session),
                              user: User = Depends(current_user)):
    user_review = (await session.execute(
        select(Review.id)
        .where(Review.game_id.__eq__(game_id), Review.user_id.__eq__(user.id))
    )).first()

    if not user_review:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='THIS_NOT_YOUR_REVIEW')

    await session.execute(delete(Review).where(Review.game_id.__eq__(game_id), Review.user_id.__eq__(user.id)))
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'REVIEW_WAS_DELETED'})

