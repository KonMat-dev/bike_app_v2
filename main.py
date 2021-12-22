import shutil
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from Bike_app_v2 import crud, schemas, models
from Bike_app_v2.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", tags=['User'])
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/users/", tags=['User'])
def create_user(
        user: schemas.UserCreate, db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)


@app.put("/user_update/", tags=['User'])
def update(request: schemas.UserCreate, db: Session = Depends(get_db),
           current_user: models.User = Depends(get_current_user)):
    db.query(models.User).filter(models.User.id == current_user.id).update(request.dict())
    db.commit()
    return "User updated "


@app.post("/posts/", tags=['Post'])
def create_post(
        title: str, description: str, file: UploadFile = File(...), db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    with open("photo/" + file.filename, "wb+")as img:
        shutil.copyfileobj(file.file, img)
    url = str("photo/" + file.filename)

    return crud.create_post(db=db, user_id=user_id, title=title, description=description, url=url)


@app.post("/post_list/", tags=['Post'])
def post_list(db: Session = Depends(get_db)):
    return crud.post_list(db=db)


@app.post("/post/{post_id}", tags=['Post'])
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Nie istnieje post o takim numerze ID")
    return post


@app.put("/post/{post_id}", tags=['Post'])
def update(post_id: int, request: schemas.PostBase, db: Session = Depends(get_db),
           current_user: models.User = Depends(get_current_user)):
    db.query(models.Post).filter(models.Post.id == post_id).update(request.dict())
    db.commit()
    return "Post updated "


@app.delete("/post/{post_id}", tags=['Post'])
def destroy(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False)
    db.commit()
    return "Post ha been deleated "


@app.post("/user_posts/", tags=['Post'])
def user_post(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_posts = crud.get_user_post(db=db, user_id=current_user.id)
    return user_posts


@app.post("/post/{value}", tags=['Post'])
def post_filter(value: str, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, id=value)
    if post is None:
        raise HTTPException(status_code=404, detail="Nie istnieje post o takim numerze ID")
    return post
