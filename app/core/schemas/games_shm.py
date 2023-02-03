from pydantic import BaseModel, validator
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

    @validator('discount')
    def check_evaluation(cls, discount):
        if discount > 1 or discount < 0.01:
            raise ValueError('The score can be in the range from 0.01 to 1')
        return float("%.2f" % discount)


class Games(BaseModel):
    result: list[GameSchema]
