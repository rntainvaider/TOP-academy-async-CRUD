from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from data import get_users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secrettopacademy"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {"user1": UserInDB(username="user1", hashed_password=get_password_hash("qwerty"))}

fake_roles_db = {"user1": "admin"}


def get_current_admin(token: str = Depends(oauth2_scheme)) -> str:
    username = get_current_user(token)
    role = get_users(username)
    _, _use, _hash, _is_admin = role
    try:
        if not _is_admin or _is_admin != 1:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return username


def authenticate_user(username: str, password: str):
    user = get_users(username=username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect user password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    username = get_current_user(token)
    return {"username": username}


@app.get("/admin")
async def read_admin_data(admin: str = Depends(get_current_admin)) -> dict[str, str]:
    return {"admin_data": f"VERY SECRET for {admin}"}
