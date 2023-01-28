from pydantic import BaseModel


class CompilationGames(BaseModel):
    title: str
    price: str
    image: str


class CompilationSchemas(BaseModel):
    result: list[CompilationGames]

