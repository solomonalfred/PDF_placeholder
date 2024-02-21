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

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 * 12

app = FastAPI()
database = DBManager("PDF_placeholder", "users")


# Todo: auth


@app.get("/extra_token")
async def extra_token(
        response: Response,
        telegram_id: str
):
    response.status_code = 201
    async with get_async_session() as session:
        telegram_find = await find_user_by_telegram(session, telegram_id)
        if telegram_find:
            access_token_expires = timedelta(minutes=5)
            access_token = create_access_token(
                data={"sub": telegram_find["nickname"]}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "Bearer"}
        response.status_code = 401
        return {"access_token": "", "token_type": "Bearer"}


@app.post("/signup")
async def sign_up(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        telegram_id: str = Form(...),
        password: str = Form(...)
):
    response.status_code = 201
    async with get_async_session() as session:
        user_data = await find_user_by_nickname(session, username)
        mail_find = await find_user_by_email(session, email)
        telegram_find = await find_user_by_telegram(session, telegram_id)
        if user_data:
            response.status_code = 208
        elif mail_find:
            response.status_code = 401
            return {"msg": "This mail is registered"}
        elif telegram_find:
            response.status_code = 401
            return {"msg": "This telegramID is registered"}
        else:
            user_id = await add_user(name,
                                     username,
                                     email,
                                     telegram_id,
                                     hashed.hash_password(password),
                                     "user_role",
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
async def list_templates(response: Response, username: str):
    try:
        async with get_async_session() as session:
            user_data = await find_user_by_nickname(session, username)
            templates = await find_docx_files(session, user_data["id"])
            return {"templates": templates}
    except:
        response.status_code = 401
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
                  data: Dict):
    async with get_async_session() as session:
        response.status_code = 200
        user = await find_user_by_nickname(session, username)
        file_path = await find_docx_file(session, user["id"], filename)
        if file_path is None:
            response.status_code = 401
            return {"response": "Template deleted"}
        if file_path["deleted"]:
            response.status_code = 401
            return {"response": "Template deleted"}
        file_path = file_path["path"]
        if len(newfilename) == 0:
            newfilename = filename
        newfilename = newfilename.replace('.pdf', '').replace('.docx', '')
        filler = Core(username, file_path, newfilename, data).process()
        result = True
        if filler.find(newfilename) == -1:
            response.status_code = 401
            result = False
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
        telegram_id: str,
        amount: int,
        unlimited: int = 0
):
    async with get_async_session() as session:
        user = await find_user_by_telegram(session, telegram_id)
        deb = await transaction_debit(session, user["id"], Decimal(amount), bool(unlimited))
    if unlimited:
        return {"balance": deb, "rate": "Unlimited"}
    return {"balance": deb, "rate": "Common"}

@app.get("/transaction_list")
async def transaction_list(
        username: str,
):
    try:
        async with get_async_session() as session:
            user = await find_user_by_nickname(session, username)
            list = await transaction_list_(session, user["id"])
            result = []
            for tmp in list:
                t = {}
                t["type"] = tmp['type']
                t["balance"] = tmp['balance']
                if tmp['unlimited']:
                    t["amount"] = "unlimited"
                else:
                    t["amount"] = tmp["amount"]
                if t["type"] == "credit":
                    t["file"] = tmp["file"]
                    t["template"] = await find_docx_file_by_id(session,
                                                               user["id"],
                                                               tmp["template"])
                    t["page_processed"] = tmp["page_processed"]
                else:
                    t["file"] = "-"
                    t["template"] = "-"
                    t["page_processed"] = "-"
                t["created_at"] = tmp["created_at"]
                result.append(t)
            return {"transactions": result}
    except:
        return {"transactions": []}


@app.post("/refresh_password")
async def refresh_password(
        response: Response,
        username: str,
        new_password: str
):
    response.status_code = 200
    async with get_async_session() as session:
        user = await find_user_by_nickname(session, username)
        renew_pass = await update_user(session,
                                       user["name"],
                                       user["nickname"],
                                       user["email"],
                                       user["telegramID"],
                                       hashed.hash_password(new_password),
                                       user["role"],
                                       user["balance"],
                                       user["unlimited"],
                                       )
        if renew_pass:
            return {"msg": "Success refreshed password"}
        response.status_code = 401
        return {"msg": "Internal server error"}


if __name__ == "__main__":
    import os
    import uvicorn

    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=int(port))
