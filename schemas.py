from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool]


# Схема для ответа
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # Включает поддержку преобразования из ORM объектов
