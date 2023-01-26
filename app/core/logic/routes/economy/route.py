from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core.logic.routes.auth.route import fastapi_users
from app.core.database.models import UserBalance, User
from app.core.database.utils import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert,  update, select

economy = APIRouter()
current_user = fastapi_users.current_user()


# fake deposit balance
@economy.get('/deposit/')
async def deposit_balance(amount: float = 1.0, session: AsyncSession = Depends(get_session),
                          user: User = Depends(current_user)):
    """
    Представим, что здесь подключена апишка оплаты.
    Происходит редирект на сервис оплаты и пользователь
    оплачивает услуги.

    Я пытался подключить сервисы оплаты, но в России они не работают :(
    """
    current_balance = (await session.execute(
        select(UserBalance.balance)
        .where(UserBalance.user_id.__eq__(user.id)))).scalar()

    if current_balance:
        await session.execute(update(UserBalance).values(user_id=user.id, balance=amount + current_balance))
    else:
        await session.execute(insert(UserBalance).values(user_id=user.id, balance=amount))
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'result': 'BALANCE_IS_REPLENISHED'})
