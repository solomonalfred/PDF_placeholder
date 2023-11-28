import requests
import json
import time
import aiohttp
import asyncio

# Todo: Потоковая отдача файлов

# server url: http://194.58.121.210:7777
# host url: http://0.0.0.0:7777

url_path = 'http://0.0.0.0:7777'

# регистрация через апи
url = f"{url_path}/api/signup"
data = {
    "name": "Nik",
    "username": "redrum",
    "email": "nik1@mail.ru",
    "password": "12345"
}
res = requests.post(url, data=data)
print('регистрация через апи')
print(res.json())
print(res.status_code)

# получение access token
url = f"{url_path}/api/access_token"
username = "redrum"
password = "12345"
data = {
        "username": username,
        "password": password
    }
res = requests.post(url, data=data)
token = res.json()
print("получение access token")
print(token)


# получение тэгов на заполнение (не обязательно)
url = f"{url_path}/api_user/placeholder_items"
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}

# files = {"file": open("test_files/Bible_God_mode.docx", "rb")}
# res = requests.post(url, files=files, headers=headers)
# data = res.json()
# print("получение тэгов на заполнение (не обязательно)")
# print(data)
#
# url = f"{url_path}/api_user/placeholder_items"
# headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}
# files = {"file": open("test_files/typical.docx", "rb")}
# res = requests.post(url, files=files, headers=headers)
# data = res.json()
# print(data)
#
# filename = {"filename": "typical.docx",
#             "newfilename": "shlyapa"}
#
#
# # заполнение и конвертация (возврат через ссылку)
# url = f"{url_path}/api_user/placeholder_link_process"
# start_time = time.time()
# res = requests.post(url, params=filename, json=data, headers=headers)
# end_time = time.time()
# execution_time = end_time - start_time
# print("заполнение и конвертация (возврат через ссылку)")
# print(execution_time)
# print(res.json())
#
# filename = {"filename": "Bible_God_mode.docx",
#             "newfilename": "shlyapa_1"}
#
# url = f"{url_path}/api_user/placeholder_link_process"
# start_time = time.time()
# res = requests.post(url, params=filename, json=data, headers=headers)
# end_time = time.time()
# execution_time = end_time - start_time
# print(execution_time)
# print(res.json())
#
# docs = ['Bible_God_mode.docx',"typical.docx"]
#
# async def request(session, it):
#     async with session.post(url, params={"filename": docs[it],
#             "newfilename": docs[it]}, json=data, headers=headers) as resp:
#         if resp.status == 200:
#             json = await resp.json()
#             print(f"IT: {it}; ", json)
#         else:
#             print(f"IT: {it}; ", {"status": "error"})
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = list()
#         for i in range(2):
#             tasks.append(request(session, i))
#         await asyncio.gather(*tasks)
#
# start_time = time.time()
# asyncio.run(main())
# end_time = time.time()  # время окончания выполнения
# execution_time = end_time - start_time
# print(execution_time)
#
#
# # заполнение и конвертация (возврат через бинарник)
# url = f"{url_path}/api_user/placeholder_process"
# res = requests.post(url, params=filename, json=data, headers=headers)
#
# with open('out_test_files/out.pdf', 'wb') as file:
#     file.write(res.content)
# print("заполнение и конвертация (возврат через бинарник)")
# print(res.status_code)
#
# # лист шаблонов
# url = f"{url_path}/api_user/template_list"
# res = requests.get(url, headers=headers)
# print("лист шаблонов")
# print(res.json())
#
# # удаление шаблона
# url = f"{url_path}/api_user/delete_template"
# delete_file = {"templatename": "typical.docx"}
# res = requests.delete(url, params=delete_file, headers=headers)
# print("удаление шаблона")
# print(res.json())
#
# url = f"{url_path}/api_user/template_list"
# res = requests.get(url, headers=headers)
# print(res.json())


url = f"{url_path}/api_user/replenishment_balance"
data = {"amount": 1,
        "unlimited": 2}
res = requests.post(url, params=data, headers=headers)
print(res.json())

