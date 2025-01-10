from sqlalchemy import Column, Integer, String, Boolean
from database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    is_admin = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)
