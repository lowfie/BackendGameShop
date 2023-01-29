from pydantic import BaseModel, validator
from datetime import datetime


class ReviewToChange(BaseModel):
    game_id: int
    title: str
    text: str
    evaluation: float

    @validator('evaluation')
    def check_evaluation(cls, evaluation):
        if evaluation % 0.5 != 0:
            raise ValueError('The score should be a multiple of 0.5')
        elif evaluation > 5 or evaluation < 1:
            raise ValueError('The score can be in the range from 1 to 5')
        return evaluation


class ReviewUser(BaseModel):
    game_id: int
    title: str
    text: str
    evaluation: float
    date_of_create: datetime
    date_of_change: datetime


class ReviewsUsers(BaseModel):
    result: list[ReviewUser]
