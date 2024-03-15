from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
from app.modules.user_modules import *

router = APIRouter(
    prefix="/link",
    tags=["link"],
)

@router.get("/file", response_class=FileResponse)
async def download_file(response: Response, filename: str, username: str):
    file_path = os.path.join(FILE_FOLDER, username, filename)
    file_exists = os.path.exists(file_path)
    response.status_code = 400
    if file_exists:
        response.status_code = 200
        return FileResponse(file_path, filename=filename)
    return {msg.MSG: msg.TEMPLATE_NOT_EXISTS}