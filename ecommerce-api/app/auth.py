from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app import models, crud
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()

# Secret key and JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
# token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = "HS256"

# OAuth2 Authorization Model: Password Credentials.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
oauth2_form_scheme = OAuth2PasswordBearer(tokenUrl="users/form-login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: str = Depends(oauth2_form_scheme),
        db: Session = Depends(get_db)
):
    """Verify the JWT and get the current user info."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # email: str = payload.get("sub")
        # if email is None:
        #     logger.info("Can't find email")
        #     raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            logger.info("Can't find username")
            raise credentials_exception
    except JWTError:
        logger.exception(JWTError)
        raise credentials_exception
    # user = crud.get_user_by_email(db, email=email)
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        logger.info("Can't find user")
        raise credentials_exception
    return user
