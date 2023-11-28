import aiohttp
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
from typing import Dict
import sys
import os
from decimal import Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.dependencies.oauth2 import *
from core.core_object import Core
from app.modules.user_modules import *
from app.modules.user_directories import *
from database.SQL_requests import *

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 31 * 12

app = FastAPI()
database = DBManager("PDF_placeholder", "users")


# Todo: auth


@app.post("/signup")
async def sign_up(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    response.status_code = 201
    async with get_async_session() as session:
        user_data = await find_user_by_nickname(session, username)
        mail_find = await find_user_by_email(session, email)
        if user_data:
            response.status_code = 208
        elif mail_find:
            response.status_code = 401
        else:
            user_id = await add_user(name,
                                     username,
                                     email,
                                     hashed.hash_password(password),
                                     session)
            create_user(username)
        return {"msg": "You're registered"}


@app.post("/access_token")
async def sign_in(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
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


# Todo: user


@app.delete("/delete_template")
async def delete_template(
        response: Response,
        username: str,
        templatename: str
):
    async with get_async_session() as session:
        user_data = await find_user_by_nickname(session, username)
        delete_path_ = await find_docx_file(session, user_data["id"], templatename)
        response.status_code = 404
        if delete_path_ is not None and delete_path_["deleted"] != True:
            delete_path = delete_path_["path"]
            os.remove(delete_path)
            result = await delete_docx_file(session,
                                            user_data["id"],
                                            templatename)
            response.status_code = 201
            return JSONResponse(content={"msg": 'Template deleted'})
        return JSONResponse(content={"msg": "There's no this template"})


@app.get("/list_templates")
async def list_templates(username: str):
    try:
        async with get_async_session() as session:
            user_data = await find_user_by_nickname(session, username)
            templates = await find_docx_files(session, user_data["id"])
            return {"templates": templates}
    except:
        return {"templates": []}


@app.get("/tags")
async def tags(path: str):
    tags = get_tags(path)
    return {"response": tags}


@app.get("/process")
async def process(response: Response,
                  filename: str,
                  newfilename: str,
                  username: str,
                  data: Dict[str, str]):
    async with get_async_session() as session:
        user = await find_user_by_nickname(session, username)
        file_path = await find_docx_file(session, user["id"], filename)
        if file_path is None:
            return {"response": "Template deleted"}
        if file_path["deleted"]:
            return {"response": "Template deleted"}
        file_path = file_path["path"]
        if len(newfilename) == 0:
            newfilename = filename
        newfilename = newfilename.replace('.pdf', '').replace('.docx', '')
        filler = Core(username, file_path, newfilename, data).process()
        result = True
        if filler.find(newfilename) == -1:
            response.status_code = 401
        else:
            file = Path(filler).name
            file_size = os.path.getsize(filler)
            count = count_pages(filler)
            result = await add_or_update_pdf_file(session,
                                                  file,
                                                  file_size,
                                                  filler,
                                                  user["id"],
                                                  count,
                                                  filename)
        if result:
            return {"response": filler}
        else:
            return {"response": "Insufficient funds"}

@app.post("/replenishment_balance")
async def debit(
        username: str,
        amount: int,
        unlimited: int = 0
):
    async with get_async_session() as session:
        user = await find_user_by_nickname(session, username)
        deb = await transaction_debit(session, user["id"], Decimal(amount), bool(unlimited))
    if unlimited:
        return {"balance": deb, "rate": "Unlimited"}
    return {"balance": deb, "rate": "Common"}

if __name__ == "__main__":
    import os
    import uvicorn

    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=int(port))
