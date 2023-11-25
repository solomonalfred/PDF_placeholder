from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse, Response
from pathlib import Path
from typing import Dict
from app.dependencies.oauth2_api import *
from app.modules.user_modules import *
from app.config import *
from urllib.parse import urlencode
import os
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


@router.post("/placeholder_items")
async def upload_docx(
        current_user: Annotated[dict, Depends(get_current_user_api)],
        file: UploadFile = File(...)
):
    '''
    Get API user file's placeholder items \n
    :param current_user: include received access token in headers in request \n
    (example: headers = {"Authorization": "<Bearer your_access_token>"})(required) \n
    :param file: template file (necessarily .docs)(required) \n
    :return: dictionary of placeholder items in json \n
    '''
    file_path = save_file(current_user["nickname"], file)
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.get(f"{server}/tags", params={'path': file_path}) as resp:
            if resp.status == 200:
                res = await resp.json()
                await database.update_field_by_nickname(current_user["nickname"],
                                                        "files_docx",
                                                        {file.filename: file_path},
                                                        transform_user)
                return JSONResponse(content=dict_tags(res["response"]))
            else:
                return {"status": "error"}


@router.post("/placeholder_process", response_class=FileResponse)
async def process_data(
        filename: str,
        newfilename: str,
        data: Dict[str, str],
        current_user: Annotated[dict, Depends(get_current_user_api)]
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
        async with session.get(f"{server}/process", params=filename, json=data) as resp:
            if resp.status == 200:
                res = await resp.json()
                return FileResponse(res["response"], filename=f"{newfilename}.pdf")
            else:
                res = await resp.json()
                return {"status": res["response"]}



@router.post("/placeholder_link_process")
async def process_data(
        filename: str,
        newfilename: str,
        data: Dict[str, str],
        current_user: Annotated[dict, Depends(get_current_user_api)]
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
        async with session.get(f"{server}/process", params=filename, json=data) as resp:
            result = {}
            if resp.status == 200:
                res = await resp.json()
                filler = res["response"]
                url = f"{SERVER_URL}/link/file?" \
                      f"{urlencode({'filename': Path(filler).name, 'username': current_user['nickname']})}"
                result = {"url": url}
            else:
                res = await resp.json()
                result = {"url": res["response"]}
            return JSONResponse(content=result)


@router.get("/template_list")
async def templates_list(current_user: Annotated[dict, Depends(get_current_user_api)]):
    username = current_user["nickname"]
    user = {"username": username}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.get(f"{server}/list_templates", params=user) as resp:
            if resp.status == 200:
                res = await resp.json()
                return JSONResponse(content=res)
            else:
                return {"status": "Server error"}


@router.delete("/delete_template")
async def delete_template(
    templatename: str,
    current_user: Annotated[dict, Depends(get_current_user_api)]
):
    username = current_user["nickname"]
    del_list = {"username": username,
                "templatename": templatename}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.delete(f"{server}/delete_template", params=del_list) as resp:
            res = await resp.json()
            return JSONResponse(content=res)

