from sqlalchemy import (
    Column,
    Integer,
    Text,
    DECIMAL,
    Float,
    String,
    ForeignKey,
    DateTime
)

from app.core.database.init import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    nickname = Column(String(30), nullable=False)
    phone = Column(String(20), nullable=True, unique=True)
    email = Column(String(20), nullable=True, unique=True)
    date_of_registry = Column(DateTime, nullable=True)


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    discount = Column(DECIMAL(3, 2), nullable=True)
    image_path = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)


class UserGames(Base):
    __tablename__ = 'user_games'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    price = Column(Float, nullable=True)


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    title = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    evaluation = Column(Float, nullable=False, default=1)
