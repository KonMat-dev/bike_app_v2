from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from . import models
from . import schemas

SECRET_KEY = "b8dcbc5ec17ace5a8fd3faa893e1b071b3766d8ba09e4bbf5d7e85ea68046357"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_post(db: Session, user_id: int, title: str, description: str, url: str):
    db_post = models.Post(title=title, description=description, owner_id=user_id, url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()


def get_user_post(db, user_id: int):
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()


def post_list(db):
    return db.query(models.Post).all()
