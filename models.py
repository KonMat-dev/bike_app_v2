import datetime

from django.forms import URLField
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
#from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

from Bike_app_v2.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    description = Column(String)
    hashed_password = Column(String)
    email = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="post")


