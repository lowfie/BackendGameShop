from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.settings.config import (
    USER_POSTGRES,
    PASSWORD_POSTGRES,
    HOST_POSTGRES,
    PORT_POSTGRES,
    DATABASE_POSTGRES
)

DB_CREDENTIALS = \
    f"postgresql+asyncpg://" \
    f"{USER_POSTGRES}:" \
    f"{PASSWORD_POSTGRES}@" \
    f"{HOST_POSTGRES}:" \
    f"{PORT_POSTGRES}/" \
    f"{DATABASE_POSTGRES}"

async_engine = create_async_engine(DB_CREDENTIALS, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
