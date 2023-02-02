from pydantic import BaseModel
from datetime import datetime


class CreateGame(BaseModel):
    title: str
    description: str
    price: float = 1
    discount: float = 0
    image_path: str


class UpdateGame(BaseModel):
    title: str
    description: str = ''
    price: float = 1
    discount: float = 0


class GameSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    discount: float
    image_path: str
    start_date: datetime


class SetGameDiscount(BaseModel):
    game_id: int
    discount: float


class Games(BaseModel):
    result: list[GameSchema]
