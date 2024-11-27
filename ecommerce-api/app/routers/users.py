from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, crud
from app.database import get_db
from app.auth import create_access_token, get_current_user
from passlib.context import CryptContext
from loguru import logger

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger.add('info.log', rotation="500 MB", retention='7 days')


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    return crud.create_user(db, user)


@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    logger.info("User login successed, access_token:{}", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


# Login
@router.post("/form-login")
def login_user(db: Session = Depends(get_db), data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    db_user = crud.get_user_by_username(db, username)
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    logger.info("User login successed, access_token:{}", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


# Get User info
@router.get("/info", response_model=schemas.UserResponse)
def get_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user
