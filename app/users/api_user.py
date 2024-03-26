from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse, Response
from typing import Dict
from app.dependencies.oauth2_api import *
from app.modules.user_modules import *
from app.config import *
from constants.api_items import *
from urllib.parse import urlencode
import itertools
import aiohttp
from database.mongo_balancer_manager import *

router = APIRouter(
    prefix="/api_user",
    tags=["api_user"],
    dependencies=[Depends(get_current_user_api)],
    responses={"404": {msg.MSG: msg.CREDENTIAL_EXEPTION}}
)

lb_manager = LoadBalancerManager(EndpointsStatus.DB_NAME,
                                 EndpointsStatus.COLLECT_NAME)
server_iterator = itertools.cycle(servers)


@router.post("/keys")
async def upload_docx(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        file: UploadFile = File(...)
):
    '''
    Get API user file's placeholder items \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :param file: template file (necessarily .docx)(required) \n
    :return: dictionary of placeholder items in json \n
    '''
    try:
        file_path = save_file(current_user[Table_items.NICKNAME], file)
        file_size = os.path.getsize(file_path)
    except:
        response.status_code = 500
        return {msg.MSG: msg.INTERNAL_SERVER_ERROR}
    user_id = current_user[Table_items.ID]
    async with aiohttp.ClientSession() as session:
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.KEYS,i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.KEYS, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.KEYS.format(server), params={Table_items.PATH: file_path}) as resp:
                await lb_manager.free_worker(EndpointsStatus.KEYS,worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    async with get_async_session() as session:
                        new_file_id = await add_or_update_docx_file(session,
                                                                    file.filename,
                                                                    file_path,
                                                                    file_size,
                                                                    user_id)
                    return JSONResponse(content=keys_response(res))
                else:
                    response.status_code = 400
                    return JSONResponse(content={msg.MSG: msg.WRONG_DOCUMENT_FORMAT})
        except Exception as e:
            await lb_manager.free_worker(EndpointsStatus.KEYS, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


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
    :param filename: template file's name (required) \n
    :param data: filled dictionary of placeholder items in json (required) \n
    (example: {"keys": {"tag1": "1", ...}, "tables": {"table1": [{"name column": "item", ...}, ...]}})\n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :param newfilename: new name of output file \n
    :return: file (.pdf) \n
    '''
    filename = {Details.FILENAME: filename,
                Details.NEW_FILENAME: newfilename,
                Details.USERNAME: current_user[Table_items.NICKNAME]}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.RENDER, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.RENDER, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.RENDER.format(server), params=filename, json=data) as resp:
                await lb_manager.free_worker(EndpointsStatus.RENDER, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    result = error_response_render(res, newfilename)
                    if result[0] != 200:
                        response.status_code = result[0]
                        return result[1]
                    newfilename = newfilename.replace('.pdf', '').replace('.docx', '')
                    return FileResponse(res[Details.RESPONCE], filename=f"{newfilename}.pdf")
                else:
                    response.status_code = 400
                    return {msg.MSG: msg.TEMPLATE_NOT_EXISTS}
        except:
            await lb_manager.free_worker(EndpointsStatus.RENDER, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


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
    :param filename: template file's name (required) \n
    :param data: filled dictionary of placeholder items in json (required) \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :param newfilename: new name of output file \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :return: link to file (.pdf) \n
    '''
    filename = {Details.FILENAME: filename,
                Details.NEW_FILENAME: newfilename,
                Details.USERNAME: current_user[Table_items.NICKNAME]}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.RENDER_LINK, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.RENDER_LINK, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.RENDER_LINK.format(server), params=filename, json=data) as resp:
                await lb_manager.free_worker(EndpointsStatus.RENDER_LINK, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    result = error_response_render(res, newfilename)
                    if result[0] != 200:
                        response.status_code = result[0]
                        return result[1]
                    filler = res[Details.RESPONCE]
                    url = LINK_URL.format(SERVER_URL,
                                          urlencode(
                                              {Details.FILENAME: Path(filler).name,
                                               Details.USERNAME: current_user[Table_items.NICKNAME]}
                                          ))
                    result = {Details.URL: url}
                else:
                    response.status_code = 401
                    return {msg.MSG: msg.TEMPLATE_NOT_EXISTS}
                return JSONResponse(content=result)
        except:
            await lb_manager.free_worker(EndpointsStatus.RENDER_LINK, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


@router.get("/templates")
async def templates_list(response: Response,
                         current_user: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Get user template's list \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :return: list of templates \n
    '''
    username = current_user[Table_items.NICKNAME]
    user = {"username": username}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.TEMPLATES, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.TEMPLATES, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.TEMPLATES.format(server), params=user) as resp:
                await lb_manager.free_worker(EndpointsStatus.TEMPLATES, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {msg.MSG: msg.INTERNAL_SERVER_ERROR}
        except:
            await lb_manager.free_worker(EndpointsStatus.TEMPLATES, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


@router.delete("/delete_template")
async def delete_template(
    response: Response,
    filename: str,
    current_user: Annotated[dict, Depends(get_current_user_api)]
):
    '''
    Delete shown template \n
    :param filename: template file's name (required) \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :return: response status of deleting template \n
    '''
    username = current_user[Table_items.NICKNAME]
    del_list = {Details.USERNAME: username,
                Details.TEMPLATENAME: filename}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.DELETE_TEMPLATE, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.DELETE_TEMPLATE, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.delete(server_path.DELETE.format(server), params=del_list) as resp:
                await lb_manager.free_worker(EndpointsStatus.DELETE_TEMPLATE, worker)
                if resp.status == 200:
                    response.status_code = resp.status
                    return {msg.MSG: msg.DELETED}
                else:
                    response.status_code = 400
                    return {msg.MSG: msg.NOT_FOUND}
        except:
            await lb_manager.free_worker(EndpointsStatus.DELETE_TEMPLATE, worker)
            response.status_code = 400
            return {msg.MSG: msg.NOT_FOUND}


@router.post("/topup_user")
async def debit(
        response: Response,
        telegram_id: str,
        amount: int,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        unlimited: int = 0,
):
    '''
    Refill user's balance or give unlimited \n
    :param telegram_id: insert user's telegram ID (example: 808652971) (required) \n
    :param amount: insert amount of money to refill user's balance (must be more than 0)(required) \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :param unlimited: insert: 0 - unlimited deactivate; 1 - unlimited activate \n
    :return: response status after refilling balance or unlimited activate \n
    '''
    async with aiohttp.ClientSession() as session:
        try:
            if current_user[Details.ROLE] != Details.ADMIN:
                response.status_code = 403
                return {msg.MSG: msg.ACCESS_DENIED}
            response.status_code = 200
            data = {Details.TELEGRAM_ID: telegram_id,
                    Details.AMOUNT: amount,
                    Details.UNLIMITED: unlimited}
            # server = next(server_iterator)
            server = ""
            worker = ""
            while True:
                flag = False
                for i in EndpointsStatus.WORKERS:
                    is_free = await lb_manager.check_worker(EndpointsStatus.TOPUP_USER, i)
                    if is_free:
                        await lb_manager.take_worker(EndpointsStatus.TOPUP_USER, i)
                        flag = True
                        worker = i
                        break
                if flag:
                    break
                await asyncio.sleep(0.5)
            server = EndpointsStatus.SERVERS[worker]
            async with session.post(server_path.BALANCE.format(server), params=data) as resp:
                await lb_manager.free_worker(EndpointsStatus.TOPUP_USER, worker)
                res = await resp.json()
                return JSONResponse(content=res)
        except:
            await lb_manager.free_worker(EndpointsStatus.TOPUP_USER, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


@router.get("/transactions")
async def transaction_list(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Get user transaction's list \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :return: list of dictionaries with transaction's record \n
    '''
    username = current_user[Table_items.NICKNAME]
    user = {Details.USERNAME: username}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.TRANSACTIONS, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.TRANSACTIONS, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.TRANSACTIONS.format(server), params=user) as resp:
                await lb_manager.free_worker(EndpointsStatus.TRANSACTIONS, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {msg.MSG: msg.INTERNAL_SERVER_ERROR}
        except:
            await lb_manager.free_worker(EndpointsStatus.TRANSACTIONS, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


@router.get("/transactions_export")
async def transaction_list_excel(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)]
):
    '''
    Get user transaction's table in excel \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :return: transaction's table in excel \n
    '''
    username = current_user[Table_items.NICKNAME]
    user = {Details.USERNAME: username}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.TRANSACTIONS_EXPORT, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.TRANSACTIONS_EXPORT, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.get(server_path.TRANSACTIONS.format(server), params=user) as resp:
                await lb_manager.free_worker(EndpointsStatus.TRANSACTIONS_EXPORT, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    output = temp_excel_builder(res)
                    return Response(content=output.read(),
                                    media_type=Excel_items.MEDIA_TYPE,
                                    headers={Excel_items.HEADER_RESPONCE_KEY: Excel_items.HEADER_RESPONCE_VALUE})
                else:
                    response.status_code = 500
                    return {msg.MSG: msg.INTERNAL_SERVER_ERROR}
        except:
            await lb_manager.free_worker(EndpointsStatus.TRANSACTIONS_EXPORT, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}


@router.post("/reset_password")
async def refresh_password(
        response: Response,
        current_user: Annotated[dict, Depends(get_current_user_api)],
        new_password: str
):
    '''
    Change user's password \n
    :param current_user: include received access token in request's header (required) \n
    (example: headers = {"Authorization": "Bearer <your_access_token>"}) \n
    :param new_password: insert new password (required) \n
    :return: response of reset password \n
    '''
    username = current_user[Table_items.NICKNAME]
    user = {Details.USERNAME: username,
            Details.NEW_PASSWORD: new_password}
    async with aiohttp.ClientSession() as session:
        # server = next(server_iterator)
        server = ""
        worker = ""
        while True:
            flag = False
            for i in EndpointsStatus.WORKERS:
                is_free = await lb_manager.check_worker(EndpointsStatus.RESET_PASSWORD, i)
                if is_free:
                    await lb_manager.take_worker(EndpointsStatus.RESET_PASSWORD, i)
                    flag = True
                    worker = i
                    break
            if flag:
                break
            await asyncio.sleep(0.5)
        server = EndpointsStatus.SERVERS[worker]
        try:
            async with session.post(server_path.PASSWORD.format(server), params=user) as resp:
                await lb_manager.free_worker(EndpointsStatus.RESET_PASSWORD, worker)
                if resp.status == 200:
                    response.status_code = 200
                    res = await resp.json()
                    return JSONResponse(content=res)
                else:
                    response.status_code = 500
                    return {msg.MSG: msg.INTERNAL_SERVER_ERROR}
        except:
            await lb_manager.free_worker(EndpointsStatus.RESET_PASSWORD, worker)
            response.status_code = 500
            return {msg.MSG: msg.INTERNAL_SERVER_ERROR}

