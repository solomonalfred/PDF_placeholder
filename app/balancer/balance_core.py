from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
from typing import Dict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.dependencies.oauth2 import *
from core.core_object import Core
from app.modules.user_modules import *
from app.modules.user_directories import *

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 31 * 12


app = FastAPI()
database = DBManager("PDF_placeholder", "users")

# auth

@app.post("/signup")
async def sign_up(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    response.status_code = 201
    if await database.find_by_nickname(username):
        response.status_code = 208
        return {"msg": "You're already registered"}
    elif await database.find_by({"email": email}):
        response.status_code = 401
        return {"msg": "This email is used by another user"}
    else:
        user = {
            "name": name,
            "nickname": username,
            "email": email,
            "key": hashed.hash_password(password),
            "files_docx": dict(),
            "files_pdf": dict()
        }
        await database.add_user(user)
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
