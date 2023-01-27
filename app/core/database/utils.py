from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database.models import User
from app.core.database.init import async_session, AsyncSession


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
