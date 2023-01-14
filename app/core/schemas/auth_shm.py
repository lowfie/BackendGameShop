from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class RegisterIn(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: None | bool = True
    is_superuser: None | bool = False
    is_verified: None | bool = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
