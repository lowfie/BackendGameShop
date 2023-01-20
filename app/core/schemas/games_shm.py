from pydantic import BaseModel
from datetime import datetime


class CreateGameOut(BaseModel):
    id: str
    title: str
    description: str
    price: float
    discount: float
    image_path: str
    start_date: datetime = datetime.now().replace(microsecond=0)


class UpdateGame(BaseModel):
    title: str
    description: str
    price: float
    discount: float
