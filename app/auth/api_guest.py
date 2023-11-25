from fastapi import APIRouter, Form
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.dependencies.oauth2 import *
from app.modules.user_directories import *


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 31 * 12

router = APIRouter(
    prefix="/api",
    tags=["api"]
)
database = DBManager("PDF_placeholder", "users")


@router.post("/signup")
async def sign_up(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    '''
    API user's registration \n
    :param name: insert name (example: user1) (required) \n
    :param username: insert username (example: user_first) (required) \n
    :param email: insert email (example: example@mail.ru) (required) \n
    :param password: insert password (example: 12345) (required) \n
    :return: response registration (example: {"msg": "You're registered"}) \n
    '''
    response.status_code = 201
    if await database.find_by_nickname(username):
        response.status_code = 208
        return {"msg": "You're already registered"}
    elif await database.find_by({"email": email}):
        response.status_code = 401
        return {"msg": "This email is used by another user"}
    else:
        user = {
            "name": name,
            "nickname": username,
            "email": email,
            "key": hashed.hash_password(password),
            "files_docx": dict(),
            "files_pdf": dict()
        }
        await database.add_user(user)
        create_user(username)
        return {"msg": "You're registered"}


@router.post("/access_token")
async def sign_in(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    '''
    Get API user's access token \n
    :param username: insert username (example: user_first) (required) \n
    :param password: insert password (example: 12345) (required) \n
    :return: \n
    '''
    response.status_code = 201
    users = await authenticate_user(form_data.username, form_data.password)
    if not users:
        response.status_code = 401
        return {"access_token": "", "token_type": "Bearer"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}
