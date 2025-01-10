from fastapi import FastAPI
from crud import create_new_user
from schemas import AddUser
from sqlalchemy.orm import Session

app = FastAPI()


# Эдпоинт для добавления пользователя
@app.post("/user/")
def create_user(user: AddUser, db: Session):
    return create_new_user(user=user, db=db)


# Эдпоинт для получения пользователя
@app.get("/user/")
def get_user():
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


# from database import engine, Base
# from models import User  # Убедитесь, что модель импортируется

# # Создание всех таблиц
# Base.metadata.create_all(bind=engine)
# print("Таблицы созданы!")
