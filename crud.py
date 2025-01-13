from models import User
from schemas import UserCreate, UserUpdate
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
def delete_user_in_base(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()  # Сохраняем изменения
    return db_user


# Изменение данныз пользователя
def update_user_in_base(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()  # Сохраняем изменения
    db.refresh(db_user)
    return db_user


# Получение списка пользователей
def get_users_in_base(db: Session):
    return db.query(User).all()
