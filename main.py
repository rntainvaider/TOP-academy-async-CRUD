from typing import Any, Generator, List
from fastapi import Depends, FastAPI, HTTPException, status
from database import SessionLocal
from crud import (
    create_new_user,
    delete_user_in_base,
    get_users_in_base,
    update_user_in_base,
)
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm.session import Session

app = FastAPI()


# Зависимость для получения сессии базы данных
def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db)) -> User:
    # Заглушка: замените на токен-аутентификацию
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def is_admin(current_user: User = Depends(get_current_user)) -> User:
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
@app.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)) -> List[User]:
    return get_users_in_base(db)


# Эдпоинт для измнения данных пользователя
@app.put("/user/{user_id}")
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = update_user_in_base(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Эдпоинт для удаления пользователя
@app.delete("user/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_db), current_user: User = Depends(is_admin)
) -> dict[str, str]:
    user = delete_user_in_base(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
