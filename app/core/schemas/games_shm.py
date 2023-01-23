from pydantic import BaseModel
from datetime import datetime


class CreateGameOut(BaseModel):
    title: str
    description: str
    price: float = 1
    discount: float = 0
    image_path: str
    start_date: datetime = datetime.now().replace(microsecond=0)


class UpdateGame(BaseModel):
    title: str
    description: str
    price: float
    discount: float
