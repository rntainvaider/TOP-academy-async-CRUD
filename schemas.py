from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Схема для ответа
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Включает поддержку преобразования из ORM объектов
