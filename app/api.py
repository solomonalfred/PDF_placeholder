import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from uvicorn import Config, Server
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from documentation import *
from auth import guest
from auth import api_guest
from users import user
from users import api_user
from links import link
from app.dependencies.sypher import PasswordManager

app = FastAPI(
    title=PDF_DOCUMENTATION.TITLE,
    version=PDF_DOCUMENTATION.VERSION,
    openapi_tags=PDF_DOCUMENTATION.tags_metadata
)

templates = Jinja2Templates(directory="../templates")
hashed = PasswordManager()
app.include_router(guest.router)
app.include_router(api_guest.router)
app.include_router(user.router)
app.include_router(api_user.router)
app.include_router(link.router)


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

if __name__ == "__main__":
    config = Config(
        app=app,
        host="0.0.0.0",
        port=7778,
        ssl_keyfile="../cert/api.pdfkabot.ru.key",
        ssl_certfile="../cert/api.pdfkabot.ru.crt"
    )
    server = Server(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())