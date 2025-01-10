from models import User
from schemas import UserCreate

# from database import SessionLocal
from sqlalchemy.orm.session import Session

# db = SessionLocal()


# # Добавление нового пользователя
# def create_new_user(user: UserCreate):
#     new_user = User(username=user.username, email=user.email, password=user.password)
#     db.add(new_user)  # Добавляем в БД
#     db.commit()  # Сохраняем изменения
#     db.refresh(new_user)  # Обновляет состояние объекта
#     return new_user


# Добавление нового пользователя
def create_new_user(db: Session, user: UserCreate):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)  # Добавляем в БД
    db.commit()  # Сохраняем изменения
    db.refresh(new_user)  # Обновляет состояние объекта
    return new_user
