from pydantic import BaseModel


class GameInCart(BaseModel):
    id: int
    title: str
    description: str
    image_path: str


class GetMyCart(BaseModel):
    result: list[GameInCart]
