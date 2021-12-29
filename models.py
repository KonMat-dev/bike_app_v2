import datetime


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from Bike_app_v2.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    description = Column(String)
    hashed_password = Column(String)
    email = Column(String)

    url = Column(String)
    address_province = Column(String)
    address_city = Column(String)
    address_street = Column(String)
    address_number = Column(String)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")
    user_comment = relationship("Comment", back_populates="comment_related")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    tape_of_service = Column(String)
    address_province = Column(String)
    address_city = Column(String)
    address_street = Column(String)
    address_number = Column(String)
    price = Column(Float)
    category_of_bike = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="post")
    img_rel = relationship("Photo", back_populates="img_rel")

class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    email = Column(String)
    description = Column(String)
    mark = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))

    comment_related = relationship("User", back_populates="user_comment")

class Photo(Base):

    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("posts.id"))
    photo_url = Column(String)

    img_rel = relationship("Post", back_populates="img_rel")
