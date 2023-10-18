from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.oauth2 import *
from app.modules.user_directories import *
from collections import defaultdict


ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
database = DBManager("PDF_placeholder", "users")
hashed = PasswordManager()
templates = Jinja2Templates(directory="../templates")

@router.get("/signup", response_class=HTMLResponse)
async def sign_up(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def sign_up(
        request: Request,
        name: str = Form(...),
        nickname: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    if await database.find_by_nickname(nickname):
        return templates.TemplateResponse("sign_up.html",
                                          {"request": request, "msg": "Пользователь уже существует"})
    elif await database.find_by({"email": email}):
        return templates.TemplateResponse("sign_up.html",
                                          {"request": request, "msg": "Пользователь с такой почтой уже зарегистрирован"})
    else:
        user = {
            "name": name,
            "nickname": nickname,
            "email": email,
            "key": hashed.hash_password(password),
            "files_docx": defaultdict(str),
            "files_pdf": defaultdict(str)
        }
        await database.add_user(user)
        flag = create_user(nickname)
        print(flag)
        return templates.TemplateResponse("sign_in.html", {"request": request})

@router.get("/signin", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})

@router.post("/signin", response_class=HTMLResponse)
async def sign_in(
        request: Request,
        nickname: str = Form(...),
        password: str = Form(...)
):
    user = await authenticate_user(nickname, password)
    if not user:
        return templates.TemplateResponse("sign_in.html",
                                          {"request": request, "msg": "Неверный никнейм или пароль."
                                                                      " Зaрегистрируйтесь или перепроверьте данные!!!"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": nickname}, expires_delta=access_token_expires
    )
    result = {
        "request": request,
        "access_token": access_token,
        "nickname": nickname
    }
    return templates.TemplateResponse("pdf_placeholder.html", result)

