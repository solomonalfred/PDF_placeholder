from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse, Response
from pathlib import Path
from typing import Dict
import pandas as pd
from io import BytesIO
from app.dependencies.oauth2_api import *
from app.modules.user_modules import *
from app.config import *
from urllib.parse import urlencode
import itertools
import aiohttp

router = APIRouter(
    prefix="/api_user",
    tags=["api_user"],
    dependencies=[Depends(get_current_user_api)],
    responses={"404": {"msg": "Credentials exception"}}
)

database = DBManager("PDF_placeholder", "users")
server_iterator = itertools.cycle(servers)

@router.post("/keys")
async def upload_docx(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        file: UploadFile = File(...)
):
    '''
    Get API user file's placeholder items \n
    :param current_user: include received access token in headers in request \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"})(required) \n
    :param file: template file (necessarily .docx)(required) \n
    :return: dictionary of placeholder items in json \n
    '''

    file_path = save_file(current_user["nickname"], file)
    file_size = os.path.getsize(file_path)
    user_id = current_user["id"]
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/tags", params={'path': file_path}) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    async with get_async_session() as session:
                        new_file_id = await add_or_update_docx_file(session,
                                                                    file.filename,
                                                                    file_path,
                                                                    file_size,
                                                                    user_id)
                    data_tags = dict_tags(res["response"][0])
                    data_tb = dict_tags(res["response"][1])
                    return JSONResponse(content={"count_tags": len(data_tags.keys()),
                                                 "count_tables": len(data_tb.keys()),
                                                 "keys": data_tags,
                                                 "tables": data_tb})
                else:
                    response.status_code = 400
                    return {"status": "Bad request"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}

@router.post("/render", response_class=FileResponse)
async def process_data(
        response: Response,
        filename: str,
        data: Dict,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        newfilename: str = ""
):
    '''
    Process API user file with filled placeholder items \n
    :param filename: transformed file's name \n
    :param newfilename: new name of output file \n
    :param data: filled dictionary of placeholder items in json \n
    :param current_user: include received access token in headers in request \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"})(required) \n
    :return: file (.pdf) \n
    '''
    filename = {"filename": filename,
                "newfilename": newfilename,
                "username": current_user["nickname"]}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/process", params=filename, json=data) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    if res["response"] == "Insufficient funds":
                        response.status_code = 402
                        return {"status": "Insufficient funds"}
                    if res["response"] == "Template deleted":
                        response.status_code = 401
                        return {"status": "Bad request. Template do not exist"}
                    return FileResponse(res["response"], filename=f"{newfilename}.pdf")
                else:
                    response.status_code = 401
                    res = await resp.json()
                    return {"status": "Bad request. Template do not exist"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}

@router.post("/render_link")
async def process_data(
        response: Response,
        filename: str,
        data: Dict,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        newfilename: str = ""
):
    '''
    Process API user file with filled placeholder items \n
    :param filename: transformed file's name \n
    :param data: filled dictionary of placeholder items in json \n
    :param current_user: include received access token in headers in request \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"})(required) \n
    :return: link to file (.pdf) \n
    '''
    filename = {"filename": filename,
                "newfilename": newfilename,
                "username": current_user["nickname"]}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/process", params=filename, json=data) as resp:
                result = {}
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    if res["response"] == "Insufficient funds":
                        response.status_code = 402
                        return {"status": "Insufficient funds"}
                    if res["response"] == "Template deleted":
                        response.status_code = 401
                        return {"status": "Bad request. Template do not exist"}
                    filler = res["response"]
                    url = f"{SERVER_URL}/link/file?" \
                          f"{urlencode({'filename': Path(filler).name, 'username': current_user['nickname']})}"
                    result = {"url": url}
                else:
                    response.status_code = 401
                    return {"status": "Bad request. Template do not exist"}
                return JSONResponse(content=result)
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}

@router.get("/templates")
async def templates_list(response: Response,
                         current_user: Annotated[dict, Depends(get_current_user_api)]):
    username = current_user["nickname"]
    user = {"username": username}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/list_templates", params=user) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {"msg": "Internal server error"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}

@router.delete("/delete_template")
async def delete_template(
    response: Response,
    filename: str,
    current_user: Annotated[dict, Depends(get_current_user_api)]
):
    username = current_user["nickname"]
    del_list = {"username": username,
                "templatename": filename}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.delete(f"{server}/delete_template", params=del_list) as resp:
                response.status_code = 200
                res = await resp.json()
                response.status_code = resp.status
                return {"msg": 'Deleted'}
        except:
            response.status_code = 401
            return {"msg": "Item not found"}

@router.post("/topup_user")
async def debit(
        response: Response,
        telegram_id: str,
        amount: int,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        unlimited: int = 0,
):
    async with aiohttp.ClientSession() as session:
        try:
            if current_user["role"] != "admin":
                response.status_code = 401
                return {"msg": "Unauthorized"}
            response.status_code = 200
            data = {"telegram_id": telegram_id,
                    "amount": amount,
                    "unlimited": unlimited}
            server = next(server_iterator)
            async with session.post(f"{server}/replenishment_balance", params=data) as resp:
                res = await resp.json()
                return JSONResponse(content=res)
        except:
            response.status_code = 401
            return {"msg": "Unauthorized"}


@router.get("/transactions")
async def transaction_list(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)]):
    username = current_user["nickname"]
    user = {"username": username}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/transaction_list", params=user) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {"msg": "Internal server error"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}


@router.get("/transactions_export")
async def transaction_list_excel(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)]
):
    username = current_user["nickname"]
    user = {"username": username}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.get(f"{server}/transaction_list", params=user) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    df = pd.DataFrame(res["transactions"])
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Лист1', index=False)
                        workbook = writer.book
                        worksheet = writer.sheets['Лист1']
                        header_format = workbook.add_format({'bold': True})
                        for col_num, value in enumerate(df.columns.values):
                            worksheet.write(0, col_num, value, header_format)
                        writer._save()
                    output.seek(0)
                    return Response(content=output.read(),
                                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    headers={"Content-Disposition": "attachment; filename=report.xlsx"})
                else:
                    response.status_code = 500
                    return {"msg": "Internal server error"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}


@router.post("/reset_password")
async def refresh_password(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        new_password: str
):

    username = current_user["nickname"]
    user = {"username": username,
            "new_password": new_password}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        try:
            async with session.post(f"{server}/refresh_password", params=user) as resp:
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {"msg": "Internal server error"}
        except:
            response.status_code = 500
            return {"msg": "Internal server error"}

