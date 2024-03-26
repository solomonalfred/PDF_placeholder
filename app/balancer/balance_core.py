from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict
import sys
import os
import uvicorn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.dependencies.oauth2 import *
from app.modules.user_modules import *
from app.modules.user_directories import *
from database.SQL_requests import *
from constants.variables import *

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
        delete_path_ = await find_docx_file(session, user_data[Tables_items.ID], templatename)
        response.status_code = 404
        if delete_path_ is not None and not delete_path_[Tables_items.DELETED]:
            delete_path = delete_path_[Tables_items.PATH]
            os.remove(delete_path)
            await delete_docx_file(session,
                                   user_data[Tables_items.ID],
                                   templatename)
            response.status_code = 200
            return JSONResponse(content={msg.MSG: msg.TP_DELETED})
        return JSONResponse(content={msg.MSG: msg.NO_TP})


@app.get("/list_templates")
async def list_templates(response: Response, username: str):
    try:
        async with get_async_session() as session:
            user_data = await find_user_by_nickname(session, username)
            templates = await find_docx_files(session, user_data[Tables_items.ID])
            return {msg.TEMPLATES: templates}
    except:
        response.status_code = 401
        return {msg.TEMPLATES: []}


@app.get("/tags")
async def tags(path: str):
    tags = get_tags(path)
    return {Details.RESPONCE: tags}


@app.get("/process")
async def process(response: Response,
                  filename: str,
                  username: str,
                  data: Dict,
                  newfilename: str = ""):
    async with get_async_session() as session:
        response.status_code = 200
        user = await find_user_by_nickname(session, username)
        file_path = await find_docx_file(session, user[Tables_items.ID], filename)
        resp = balancer_process_response(file_path, newfilename, filename, username, data)
        if not resp[0]:
            response.status_code = resp[1]
            return resp[2]
        result = await add_or_update_pdf_file(session,
                                              resp[2][Details.RESPONCE][0],
                                              resp[2][Details.RESPONCE][1],
                                              resp[2][Details.RESPONCE][3],
                                              user[Tables_items.ID],
                                              resp[2][Details.RESPONCE][2],
                                              filename)
        if result:
            return {Details.RESPONCE: resp[2][Details.RESPONCE][3]}
        else:
            return {Details.RESPONCE: msg.INSUFFICIENT_FUNDS}


@app.post("/replenishment_balance")
async def debit(
        telegram_id: str,
        amount: int,
        unlimited: int = 0
):
    async with get_async_session() as session:
        user = await find_user_by_telegram(session, telegram_id)
        deb = await transaction_debit(session, user[Tables_items.ID], Decimal(amount), bool(unlimited))
    if unlimited:
        return {msg.BALANCE: deb, Details.RATE: Details.UNLIMITED}
    return {msg.BALANCE: deb, Details.RATE: Details.COMMON}


@app.get("/transaction_list")
async def transaction_list(
        username: str,
):
    try:
        async with get_async_session() as session:
            user = await find_user_by_nickname(session, username)
            list = await transaction_list_(session, user[Tables_items.ID])
            result = []
            for tmp in list:
                res = balancer_transaction_fill_record(tmp)
                if tmp[Tables_items.TYPE] == Details.CREDIT:
                    res[Tables_items.TEMPLATE] = await find_docx_file_by_id(session,
                                                                            user[Tables_items.ID],
                                                                            tmp[Tables_items.TEMPLATE])
                result.append(res)
            return {Details.TRANSACTIONS: result}
    except:
        return {Details.TRANSACTIONS: []}


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
                                       user[Tables_items.NAME],
                                       user[Tables_items.NICKNAME],
                                       user[Tables_items.EMAIL],
                                       user[Tables_items.TELEGRAM_ID],
                                       hashed.hash_password(new_password),
                                       user[Tables_items.ROLE],
                                       user[Tables_items.BALANCE],
                                       user[Tables_items.UNLIMITED])
        if renew_pass:
            return {msg.MSG: msg.SUCCESS_REFRESH}
        response.status_code = 401
        return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


if __name__ == "__main__":

    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=int(port))
