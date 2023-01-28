from pydantic import BaseModel, validator


class ReviewSchema(BaseModel):
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
