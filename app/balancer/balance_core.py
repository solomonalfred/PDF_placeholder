from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pathlib import Path
from typing import Dict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.core_object import Core
from database.db import DBManager
from app.modules.user_modules import *


app = FastAPI()
database = DBManager("PDF_placeholder", "users")




# user
@app.delete("/delete_template")
async def delete_template(
        response: Response,
        username: str,
        templatename: str
):
    file_path = await database.find_by_nickname(username)
    delete_path_ = file_path["files_docx"]
    response.status_code = 404
    if delete_path_.get(templatename) is not None:
        delete_path = file_path["files_docx"][templatename]
        os.remove(delete_path)
        await database.update_field_by_nickname(username,
                                                "files_docx",
                                                {'key': templatename},
                                                delete_transform)
        response.status_code = 201
        return JSONResponse(content={"msg": 'Template deleted'})
    return JSONResponse(content={"msg": "There's no this template"})


@app.get("/list_templates")
async def list_templates(username: str):
    try:
        file_path = await database.find_by_nickname(username)
        templates = list(file_path["files_docx"].keys())
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
    file_path = await database.find_by_nickname(username)
    file_path = file_path["files_docx"][filename]
    if len(newfilename) == 0:
        newfilename = filename
    newfilename = newfilename.replace('.pdf', '').replace('.docx', '')
    filler = Core(username, file_path, newfilename, data).process()
    if filler.find(newfilename) == -1:
        response.status_code = 401
    else:
        file = Path(filler).name
        await database.update_field_by_nickname(username,
                                            "files_pdf",
                                            {file: filler},
                                            transform_user)
    return {"response": filler}


if __name__ == "__main__":
    import os
    import uvicorn
    port = os.getenv("PORT")
    uvicorn.run(app, host="0.0.0.0", port=int(port))
