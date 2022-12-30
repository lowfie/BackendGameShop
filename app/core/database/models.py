from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.core.database.init import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    nickname = Column(String(30), nullable=True)
    phone = Column(String(20), nullable=True, unique=True)
    email = Column(String(20), nullable=True, unique=True)
    date_of_registry = Column(DateTime, nullable=False)

