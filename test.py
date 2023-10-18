import requests
import json

# Todo: Потоковая отдача файлов

# server url: http://194.58.121.210:7777
# host url: http://0.0.0.0:7777

# регистрация через апи
url = "http://0.0.0.0:7777/api/signup"
data = {
    "name": "Nik",
    "username": "redrum",
    "email": "nik1@mail.ru",
    "password": "12345"
}
res = requests.post(url, data=data)
print(res.json())
print(res.status_code)

# получение access token
url = "http://0.0.0.0:7777/api/access_token"
username = "redrum"
password = "12345"
data = {
        "username": username,
        "password": password
    }
res = requests.post(url, data=data)
token = res.json()
print(token)


# получение тэгов на заполнение (не обязательно)
url = "http://0.0.0.0:7777/api_user/placeholder_items"
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}
files = {"file": open("test_files/typical.docx", "rb")}
res = requests.post(url, files=files, headers=headers)
data = res.json()
print(data)

# data["Browser"] = "Gooogle"
# data["Version"] = "0.0.0.0.1"
# data["IP"] = "0.0.0.127"
# data["Location"] = "Russia"
# data["Created"] = "Konstantine"

filename = {"filename": "typical.docx",
            "newfilename": "shlyapa"}


# заполнение и конвертация (возврат через ссылку)
url = "http://0.0.0.0:7777/api_user/placeholder_link_process"
res = requests.post(url, params=filename, json=data, headers=headers)
print(res.json())


# заполнение и конвертация (возврат через бинарник)
url = "http://0.0.0.0:7777/api_user/placeholder_process"
res = requests.post(url, params=filename, json=data, headers=headers)

with open('out_test_files/out.pdf', 'wb') as file:
    file.write(res.content)
print(res.status_code)

# лист шаблонов
url = "http://0.0.0.0:7777/api_user/template_list"
res = requests.get(url, headers=headers)
print(res.json())

# удаление шаблона
url = "http://0.0.0.0:7777/api_user/delete_template"
delete_file = {"templatename": "typical.docx"}
res = requests.delete(url, params=delete_file, headers=headers)
print(res.json())

url = "http://0.0.0.0:7777/api_user/template_list"
res = requests.get(url, headers=headers)
print(res.json())

