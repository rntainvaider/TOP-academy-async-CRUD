from models import User
from schemas import UserCreate
from passlib.hash import bcrypt

# from database import SessionLocal
from sqlalchemy.orm.session import Session


# Добавление нового пользователя
def create_new_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_admin=user.is_admin,
    )
    db.add(new_user)  # Добавляем в БД
    db.commit()  # Сохраняем изменения
    db.refresh(new_user)  # Обновляет состояние объекта
    return new_user


# Удаление пользователя из базы
def delete_user(db: Session, user):
    pass
