from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from typing import Dict
from app.dependencies.oauth2_api import *
from app.modules.user_modules import *
from app.config import *
from core.core_object import Core
from urllib.parse import urlencode

router = APIRouter(
    prefix="/api_user",
    tags=["api_user"],
    dependencies=[Depends(get_current_user_api)],
    responses={"404": {"msg": "Credentials exception"}}
)

database = DBManager("PDF_placeholder", "users")


@router.post("/placeholder_items")
async def upload_docx(current_user: Annotated[dict, Depends(get_current_user_api)], file: UploadFile = File(...)):
    '''
    Get API user file's placeholder items
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "Bearer your_access_token"})(required)
    :param file: template file (necessarily .docs)(required)
    :return: dictionary of placeholder items in json
    '''
    file_path = save_file(current_user["nickname"], file)
    tags = get_tags(file_path)
    await database.update_field_by_nickname(current_user["nickname"],
                                            "files_docx",
                                            {file.filename: file_path},
                                            transform_user)
    return JSONResponse(content=dict_tags(tags))


@router.post("/placeholder_process", response_class=FileResponse)
async def process_data(filename: str, data: Dict[str, str], current_user: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Process API user file with filled placeholder items
    :param filename: transformed file's name
    :param data: filled dictionary of placeholder items in json
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "Bearer your_access_token"})(required)
    :return: file (.pdf)
    '''
    username = current_user["nickname"]
    file_path = await database.find_by_nickname(username)
    file_path = file_path["files_docx"][filename]
    filler = Core(current_user["nickname"], file_path, data).process()
    file = Path(filler).name
    await database.update_field_by_nickname(current_user["nickname"],
                                            "files_pdf",
                                            {"_".join(file.split("_")[1::]): filler},
                                            transform_user)
    return FileResponse(filler, filename=filename)


@router.post("/placeholder_link_process")
async def process_data(filename: str, data: Dict[str, str], current_user: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Process API user file with filled placeholder items
    :param filename: transformed file's name
    :param data: filled dictionary of placeholder items in json
    :param current_user: include received access token in headers in request
    (example: headers = {"Authorization": "Bearer your_access_token"})(required)
    :return: link to file (.pdf)
    '''
    username = current_user["nickname"]
    file_path = await database.find_by_nickname(username)
    file_path = file_path["files_docx"][filename]
    filler = Core(current_user["nickname"], file_path, data).process()
    file = Path(filler).name
    await database.update_field_by_nickname(current_user["nickname"],
                                            "files_pdf",
                                            {"_".join(file.split("_")[1::]): filler},
                                            transform_user)
    # server url: http://81.200.156.178:7777
    # host url: http://0.0.0.0:7777
    url = f"{SERVER_URL}/link/file?{urlencode({'filename': file, 'username': current_user['nickname']})}"
    result = {"url": url}
    return JSONResponse(content=result)
