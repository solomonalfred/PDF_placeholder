import requests
import time
import aiohttp
import asyncio

# server url: https://194.58.121.210:7777
# host url: http://0.0.0.0:7777
# prod url: https://api.pdfkabot.ru

url_path = 'http://0.0.0.0:7777'

# регистрация через апи
url = f"{url_path}/api/signup"
data = {
    "name": "Nikita",
    "username": "laplas",
    "email": "nik2@mail.ru",
    "telegram_id": "808652965",
    "password": "54321"
}
res = requests.post(url, data=data)
print('регистрация через апи')
print(res.json())
print(res.status_code)

# получение access token
url = f"{url_path}/api/access_token"
data = {
        "username": "laplas",
        "password": "54321"
    }
res = requests.post(url, data=data)
token = res.json()
print("получение access token")
print(token)
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}

url = f"{url_path}/api_user/keys"
files = {"file": open("test_files/typical.docx", "rb")}
res = requests.post(url, files=files, headers=headers)
data = res.json()
print(data)

filename = {"filename": "typical.docx",
            "newfilename": "shlyapa"}

# заполнение и конвертация (возврат через ссылку)
url = f"{url_path}/api_user/render_link"
start_time = time.time()
res = requests.post(url, params=filename, json=data["keys"], headers=headers)
end_time = time.time()
execution_time = end_time - start_time
print("заполнение и конвертация (возврат через ссылку)")
print(execution_time)
print(res.json())

#

# получение тэгов на заполнение (не обязательно)
url = f"{url_path}/api_user/keys"
files = {"file": open("test_files/Bible_God_mode.docx", "rb")}
res = requests.post(url, files=files, headers=headers)
data = res.json()
print("получение тэгов на заполнение (не обязательно)")
print(data)

url = f"{url_path}/api_user/keys"
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}
files = {"file": open("test_files/typical.docx", "rb")}
res = requests.post(url, files=files, headers=headers)
data = res.json()
print(data)

filename = {"filename": "typical.docx",
            "newfilename": "shlyapa"}


# заполнение и конвертация (возврат через ссылку)
url = f"{url_path}/api_user/render_link"
start_time = time.time()
res = requests.post(url, params=filename, json=data["keys"], headers=headers)
end_time = time.time()
execution_time = end_time - start_time
print("заполнение и конвертация (возврат через ссылку)")
print(execution_time)
print(res.json())

filename = {"filename": "Bible_God_mode.docx",
            "newfilename": "shlyapa_1"}

url = f"{url_path}/api_user/render_link"
start_time = time.time()
res = requests.post(url, params=filename, json=data["keys"], headers=headers)
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)
print(res.json())

docs = ['Bible_God_mode.docx',"typical.docx"]

async def request(session, it):
    async with session.post(url,
                            params={"filename": docs[it],
                            "newfilename": docs[it]},
                            json=data["keys"],
                            headers=headers) as resp:
        if resp.status == 200:
            json = await resp.json()
            print(f"IT: {it}; ", json)
        else:
            print(f"IT: {it}; ", {"status": "error"})


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i in range(2):
            tasks.append(request(session, i))
        await asyncio.gather(*tasks)

start_time = time.time()
asyncio.run(main())
end_time = time.time()  # время окончания выполнения
execution_time = end_time - start_time
print(execution_time)

filename = {"filename": "typical.docx",
            "newfilename": "shlyapa"}

# заполнение и конвертация (возврат через бинарник)
url = f"{url_path}/api_user/render"
res = requests.post(url, params=filename, json=data["keys"], headers=headers)

with open('out_test_files/out.pdf', 'wb') as file:
    file.write(res.content)
print("заполнение и конвертация (возврат через бинарник)")
print(res.status_code)

# лист шаблонов
url = f"{url_path}/api_user/templates"
res = requests.get(url, headers=headers)
print("лист шаблонов")
print(res.json())

# удаление шаблона
url = f"{url_path}/api_user/delete_template"
delete_file = {"filename": "typical.docx"}
res = requests.delete(url, params=delete_file, headers=headers)
print("удаление шаблона")
print(res.json())

url = f"{url_path}/api_user/templates"
res = requests.get(url, headers=headers)
print(res.json())

# пополнение баланса
url = f"{url_path}/api_user/topup_user"
data = {"amount": 1,
        "telegram_id": "laplas",
        "unlimited": 2}
res = requests.post(url, params=data, headers=headers)
print(res.json())

# регистрация от админа и пополнение баланса от него
url = f"{url_path}/api/access_token"
data = {
        "username": "admin",
        "password": "12345"
    }
res = requests.post(url, data=data)
token_ = res.json()
print("получение access token")
print(token_)
headers = {"Authorization": f"{token_['token_type']} {token_['access_token']}"}

url = f"{url_path}/api_user/topup_user"
data = {"amount": 1,
        "telegram_id": "808652965",
        "unlimited": 1}
res = requests.post(url, params=data, headers=headers)
print(res.json())

# список транзакция по пользоваетелю
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}
url = f"{url_path}/api_user/transactions"
res = requests.get(url, headers=headers)
for i in res.json()["transactions"]:
    print(i)

# список транзакция по пользоваетелю в excel
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}
url = f"{url_path}/api_user/transactions_export"
res = requests.get(url, headers=headers)
with open('out_test_files/out.xlsx', 'wb') as file:
    file.write(res.content)

# сбос(изменение) пароля
url = f"{url_path}/api/extra_token"
data = {"telegram_id": "808652965"}
res = requests.get(url, data=data)
token_extra = res.json()
print("Временный токен на 5 минут")
print(token_extra)

url = f"{url_path}/api_user/reset_password"
headers = {"Authorization": f"{token_extra['token_type']} {token_extra['access_token']}"}
data = {"new_password": "54321"}
res = requests.post(url, params=data, headers=headers)
print("Изменение пароля")
print(res.json())

url = f"{url_path}/api/access_token"
data = {
        "username": "laplas",
        "password": "54321"
    }
res = requests.post(url, data=data)
token = res.json()
print("получение access token")
print(token)

# генерация таблицы
data ={ "cryptocurrencies": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "price_usd": 39857.20,
      "price_eur": 34991.42,
      "price_gbp": 29489.55
    },
    {
      "name": "Ethereum",
      "symbol": "ETH",
      "price_usd": 2845.62,
      "price_eur": 2498.75,
      "price_gbp": 2104.89
    },
    {
      "name": "Ripple",
      "symbol": "XRP",
      "price_usd": 0.84,
      "price_eur": 0.74,
      "price_gbp": 0.62
    }
  ],
"traffic": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "price_usd": 39857.20,
      "price_eur": 34991.42,
      "price_gbp": 29489.55
    },
    {
      "name": "Ethereum",
      "symbol": "ETH",
      "price_usd": 2845.62,
      "price_eur": 2498.75,
      "price_gbp": 2104.89
    },
    {
      "name": "Ripple",
      "symbol": "XRP",
      "price_usd": 0.84,
      "price_eur": 0.74,
      "price_gbp": 0.62
    }
  ]
}
url = f"{url_path}/api_user/render_table"
res = requests.get(url, json=data, headers=headers)

with open('out_test_files/out.pdf', 'wb') as file:
    file.write(res.content)

