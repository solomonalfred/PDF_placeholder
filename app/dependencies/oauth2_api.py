from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database.db import DBManager
from sypher import PasswordManager


SECRET_KEY = "43d108a66940040ac38a714e192c57b8b3b1813e43efe39e022201a4dcf68bf2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme_api = OAuth2PasswordBearer(tokenUrl="/api/access_token")
database = DBManager("PDF_placeholder", "users")
hashed = PasswordManager()


async def authenticate_user(username: str, password: str):
    user = await database.find_by_nickname(username)
    if not user:
        return False
    if not hashed.verify_password(password, user["key"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60 * 24 * 31 * 12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user_api(token: Annotated[str, Depends(oauth2_scheme_api)]):
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
    user = await database.find_by_nickname(username)
    if user is None:
        raise credentials_exception
    return user