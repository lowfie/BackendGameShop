from fastapi_users import schemas
from pydantic import EmailStr
from datetime import datetime


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: None | str
    last_name: None | str
    nickname: None | str
    phone: None | str
    email: EmailStr
    date_of_registry: None | datetime
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
    first_name: None | str = None
    last_name: None | str = None
    nickname: None | str = None
    phone: None | str = None
    password: None | str
    email: None | EmailStr
    is_active: None | bool = True
    is_superuser: None | bool = False
    is_verified: None | bool = False
