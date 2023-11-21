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
    Get API user file's placeholder items
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "<Bearer your_access_token>"})(required)
    :param file: template file (necessarily .docs)(required)
    :return: dictionary of placeholder items in json
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
    Process API user file with filled placeholder items
    :param filename: transformed file's name
    :param newfilename: new name of output file
    :param data: filled dictionary of placeholder items in json
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "Bearer <your_access_token>"})(required)
    :return: file (.pdf)
    '''
    filename = {"filename": filename,
                "newfilename": newfilename,
                "username": current_user["nickname"]}
    async with aiohttp.ClientSession() as session:
        server = next(server_iterator)
        async with session.get(f"{server}/process", params=filename, json=data) as resp:
            if resp.status == 200:
                res = await resp.json()
                return FileResponse(FILE_FOLDER + res["response"], filename=f"{newfilename}.pdf")
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
    Process API user file with filled placeholder items
    :param filename: transformed file's name
    :param data: filled dictionary of placeholder items in json
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "Bearer <your_access_token>"})(required)
    :return: link to file (.pdf)
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
    file_path = await database.find_by_nickname(username)
    templates = list(file_path["files_docx"].keys())
    return JSONResponse(content={"templates": templates})

@router.delete("/delete_template")
async def delete_template(
    response: Response,
    templatename: str,
    current_user: Annotated[dict, Depends(get_current_user_api)]
):
    username = current_user["nickname"]
    file_path = await database.find_by_nickname(username)
    delete_path_ = file_path["files_docx"]
    response.status_code = 404
    if delete_path_.get(templatename) is not None:
        delete_path = file_path["files_docx"][templatename]
        os.remove(delete_path)
        await database.update_field_by_nickname(current_user["nickname"],
                                                "files_docx",
                                                {'key': templatename},
                                                delete_transform)
        response.status_code = 201
        return JSONResponse(content={"msg": 'Template deleted'})
    return JSONResponse(content={"msg": "There's no this template"})
