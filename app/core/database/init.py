from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings.config import (
    USER_POSTGRES,
    PASSWORD_POSTGRES,
    HOST_POSTGRES,
    PORT_POSTGRES,
    DATABASE_POSTGRES
)

db_credentials = \
    f"postgresql://" \
    f"{USER_POSTGRES}:" \
    f"{PASSWORD_POSTGRES}@" \
    f"{HOST_POSTGRES}:" \
    f"{PORT_POSTGRES}/" \
    f"{DATABASE_POSTGRES}"

async_engine = create_async_engine(db_credentials, echo=True)
Base = declarative_base()
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

