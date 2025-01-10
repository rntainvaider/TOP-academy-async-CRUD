from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Строка подключения к PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/top_dz"

# Создание движка
engine = create_engine(DATABASE_URL, echo=True)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()
