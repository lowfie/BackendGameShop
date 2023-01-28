from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import Review, User
from app.core.schemas.reviews_shm import ReviewSchema
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

import datetime

reviews = APIRouter()
current_user = fastapi_users.current_user()


@reviews.post('/create_overview/')
async def leave_review(review: ReviewSchema,
                       session: AsyncSession = Depends(get_session),
                       user: User = Depends(current_user)):
    is_game = (await session.execute(
        select(Review.game_id)
        .where(Review.game_id.__eq__(review.game_id))
    )).first()

    if is_game:
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
async def edit_left_review(review: ReviewSchema,
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


@reviews.get('/my_reviews/')
async def my_reviews(session: AsyncSession = Depends(get_session),
                     user: User = Depends(current_user)):
    pass


@reviews.get('/latest_reviews/')
async def latest_reviews(session: AsyncSession = Depends(get_session),
                         user: User = Depends(current_user)):
    pass


@reviews.delete('/delete_my_review/')
async def get_latest_reviews(session: AsyncSession = Depends(get_session),
                             user: User = Depends(current_user)):
    pass
