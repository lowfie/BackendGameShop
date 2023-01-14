from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database.models import User
from app.core.database.init import async_engine


async def get_session() -> AsyncSession:
    async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
