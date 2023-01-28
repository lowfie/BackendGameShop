from pydantic import BaseModel


class LibraryGame(BaseModel):
    title: str
    description: str
    image_path: str
    start_date: str


class LibrarySchema(BaseModel):
    result: list[LibraryGame]
