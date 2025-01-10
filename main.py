from fastapi import Depends, FastAPI
from database import SessionLocal
from crud import create_new_user
from models import User
from schemas import UserCreate, UserResponse
from sqlalchemy.orm.session import Session

app = FastAPI()


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эдпоинт для добавления пользователя
@app.post("/user/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    return create_new_user(db=db, user=user)


# Эдпоинт для получения пользователя
@app.get("/user/", response_model=UserResponse)
def get_user():
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
