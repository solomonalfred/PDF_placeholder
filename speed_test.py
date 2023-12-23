from generate_file import create_word_document
import requests
import time
import aiohttp
import asyncio

url_path = 'http://194.58.121.210:7777'

url = f"{url_path}/api/access_token"
username = "redrum"
password = "12345"
data = {
        "username": username,
        "password": password
    }
res = requests.post(url, data=data)
token = res.json()
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}

def count_page(page: int):
    url = f"{url_path}/api_user/placeholder_items"
    create_word_document(page, 'random_text_document.docx')
    files = {"file": open("random_text_document.docx", "rb")}
    start_time = time.time()
    res = requests.post(url, files=files, headers=headers)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Получение тэгов\n"
          f"Колличество страниц: {page}\n"
          f"Код обработки: {res.status_code}\n"
          f"Время работы: {execution_time}")
    data = res.json()
    for key in data:
        data[key] = 'Hello world'
    filename = {"filename": "random_text_document.docx",
                "newfilename": "shlyapa"}
    url = f"{url_path}/api_user/placeholder_link_process"
    start_time = time.time()
    res = requests.post(url, params=filename, json=data, headers=headers)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Обработка документа\n"
          f"Колличество страниц: {page}\n"
          f"Код обработки: {res.status_code}\n"
          f"Время работы: {execution_time}\n"
          f"url: {res.json()['url']}\n\n")
    url = f"{url_path}/api_user/delete_template"
    delete_file = {"templatename": "random_text_document.docx"}
    requests.delete(url, params=delete_file, headers=headers)


count_page(1)
count_page(5)
count_page(10)
count_page(25)
count_page(50)
count_page(100)
