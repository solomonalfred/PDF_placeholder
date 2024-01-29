import pandas as pd
from generate_file import create_docx
import requests
import time

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

tag_index = ["1 тэг(ов)", "5 тэг(ов)", "10 тэг(ов)", "25 тэг(ов)", "50 тэг(ов)", "100 тэг(ов)"]

data_tag = {}
data_process = {}

for i in [1, 5, 10, 25, 50, 100]:
    data_tag[f"{i} стр."] = []
    data_process[f"{i} стр."] = []
    for j in [1, 5, 10, 25, 50, 100]:
        url = f"{url_path}/api_user/placeholder_items"
        create_docx(j, i)
        files = {"file": open("output.docx", "rb")}
        start_time = time.time()
        res = requests.post(url, files=files, headers=headers)
        end_time = time.time()
        execution_time = end_time - start_time
        data_tag[f"{i} стр."].append(execution_time)
        data = res.json()
        for key in data:
            data[key] = 'Hello world'
        filename = {"filename": "output.docx"}
        url = f"{url_path}/api_user/placeholder_link_process"
        start_time = time.time()
        res = requests.post(url, params=filename, json=data, headers=headers)
        end_time = time.time()
        execution_time = end_time - start_time
        data_process[f"{i} стр."].append(execution_time)
        url = f"{url_path}/api_user/delete_template"
        delete_file = {"filename": "output.docx"}
        requests.delete(url, params=delete_file, headers=headers)

d_tag = pd.DataFrame(data_tag, index=tag_index)
d_proc = pd.DataFrame(data_process, index=tag_index)

d_tag.to_excel("speed_tag.xlsx")
d_proc.to_excel("speed_process.xlsx")
