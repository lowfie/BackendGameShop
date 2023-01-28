from sqlalchemy import (
    Column,
    Integer,
    Text,
    DECIMAL,
    Float,
    String,
    ForeignKey,
    DateTime,
    Boolean
)

from app.core.database.init import Base
from fastapi_users.db import SQLAlchemyBaseUserTable

from datetime import datetime


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, nullable=False)
    first_name: str = Column(String(30), nullable=True)
    last_name: str = Column(String(30), nullable=True)
    nickname: str = Column(String(30), nullable=True)
    phone: str = Column(String(20), nullable=True, unique=True)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    date_of_registry: datetime = Column(DateTime, nullable=True, default=datetime.now().replace(microsecond=0))
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


class Game(Base):
    __tablename__ = 'games'

    id: int = Column(Integer, primary_key=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    title: str = Column(String(50), nullable=True)
    description: str = Column(Text, nullable=True)
    price: float = Column(Float, nullable=True)
    discount: float = Column(DECIMAL(3, 2), nullable=True)
    image_path: str = Column(Text, nullable=True)
    start_date: datetime = Column(DateTime, nullable=True, default=datetime.now().replace(microsecond=0))


class UserGames(Base):
    __tablename__ = 'user_games'

    id: int = Column(Integer, primary_key=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id: int = Column(Integer, ForeignKey('games.id'), nullable=False)


class Cart(Base):
    __tablename__ = 'cart'

    id: int = Column(Integer, primary_key=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id: int = Column(Integer, ForeignKey('games.id'), nullable=False)


class Review(Base):
    __tablename__ = 'reviews'

    id: int = Column(Integer, primary_key=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id: int = Column(Integer, ForeignKey('games.id'), nullable=False)
    title: str = Column(String(50), nullable=False)
    text: str = Column(Text, nullable=False)
    evaluation: float = Column(Float, nullable=False, default=1)
    date_of_create: datetime = Column(nullable=True, default=datetime.now().replace(microsecond=0))
    date_of_change: datetime = Column(nullable=True)


class UserBalance(Base):
    __tablename__ = 'user_balances'

    id: int = Column(Integer, primary_key=True, nullable=False, default=0)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    balance: float = Column(Float, nullable=False, default=0)
