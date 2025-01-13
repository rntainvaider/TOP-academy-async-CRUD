from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


# Схема для ответа
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Включает поддержку преобразования из ORM объектов
