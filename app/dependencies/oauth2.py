from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.mongo_manager import DBManager
from app.dependencies.sypher import PasswordManager
from database.SQL_requests import *
from configurations import SECRET_KEY, ALGORITHM


ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")
# database = DBManager("PDF_placeholder", "users")
hashed = PasswordManager()


async def authenticate_user(username: str, password: str):
    async with get_async_session() as session:
        user = await find_user_by_nickname(session, username)
        if not user:
            return False
        if not hashed.verify_password(password, user["password"]):
            return False
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60 * 24 * 30 * 12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    async with get_async_session() as session:
        user = await find_user_by_nickname(session, username)
        if user is None:
            raise credentials_exception
        return user
