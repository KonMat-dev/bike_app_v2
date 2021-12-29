import datetime
from typing import List, Optional

from fastapi import Body
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    password: str
    email: str
    address_province: str
    address_city: str
    address_street: str
    address_number: str


class PostBase(BaseModel):
    title: str
    description: str
    tape_of_service: str
    address_province: str
    address_city: str
    address_street: str
    address_number: str
    price: int
    category_of_bike: str


class PostList(PostBase):
    created_date: Optional[datetime.datetime]
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class Comments(BaseModel):
    name: str
    email: str
    description: str


class CommentsList(Comments):
    id: int
    mark: int
    owner_id: int
    created_date: Optional[datetime.datetime] = Body(None)

    class Config:
        orm_mode = True
