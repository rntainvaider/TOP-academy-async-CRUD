from fastapi import Depends, FastAPI, HTTPException, status
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


def get_current_user(db: Session = Depends(get_db)):
    # Заглушка: замените на токен-аутентификацию
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def is_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


# Эдпоинт для добавления пользователя
@app.post("/user/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin),
) -> User:
    return create_new_user(db=db, user=user)


# Эдпоинт для получения пользователей
@app.get("/user/", response_model=UserResponse)
def get_user():
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
