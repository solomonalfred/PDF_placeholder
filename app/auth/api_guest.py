from fastapi import APIRouter, Form
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import itertools
import aiohttp

from app.config import *
from app.dependencies.oauth2 import *
from configurations import ADMIN


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 31 * 12

router = APIRouter(
    prefix="/api",
    tags=["api"]
)
database = DBManager("PDF_placeholder", "users")
server_iterator = itertools.cycle(servers)



@router.post("/signup")
async def sign_up(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        telegram_id: str = Form(...),
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
    user_data = {"name": name,
                 "username": username,
                 "email": email,
                 "telegram_id": telegram_id,
                 "password": password}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.post(f"{server}/signup", data=user_data) as resp:
            if resp.status == 201:
                response.status_code = 201
            elif resp.status == 208:
                response.status_code = 208
            else:
                response.status_code = 401
            res = await resp.json()
            return res


@router.post("/access_token")
async def sign_in(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    '''
    Get API user's access token \n
    :param username: insert username (example: user_first) (required) \n
    :param password: insert password (example: 12345) (required) \n
    :return: token and token type for use user's requests \n
    (example: {'access_token': 'eyJhbGc...', 'token_type': 'Bearer'})\n
    '''
    data = {
        "username": form_data.username,
        "password": form_data.password
    }
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.post(f"{server}/access_token", data=data) as resp:
            async with get_async_session() as session:
                await add_user_if_not_exists(session,
                                             "admin",
                                             "admin",
                                             "nik_bogdanov2002@mail.ru",
                                             "80865296a",
                                             hashed.hash_password(ADMIN),
                                             "admin")
            if resp.status == 201:
                response.status_code = 201
            else:
                response.status_code = 401
            res = await resp.json()
            return res

@router.get("/extra_token")
async def extra_token(
        response: Response,
        telegram_id: str = Form(...)
):
    '''
    Get extra token to reset user's password (timelimit 5 minutes) \n
    :param telegram_id: insert user's telegram ID (example: 808652971)\n
    :return: extra token and token type for use user's requests \n
    (example: {'access_token': 'eyJhbGc...', 'token_type': 'Bearer'})\n
    '''
    data = {"telegram_id": telegram_id}
    response.status_code = 201
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.get(f"{server}/extra_token", params=data) as resp:
            response.status_code = resp.status
            res = await resp.json()
            return JSONResponse(content=res)
