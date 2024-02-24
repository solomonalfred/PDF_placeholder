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
    "username": "kruger",
    "email": "nik4@mail.ru",
    "telegram_id": "808652971",
    "password": "54321"
}
res = requests.post(url, data=data)
print('регистрация через апи')
print(res.json())
print(res.status_code)

# получение access token
url = f"{url_path}/api/access_token"
data = {
        "username": "kruger",
        "password": "54321"
    }
res = requests.post(url, data=data)
token = res.json()
print("получение access token")
print(token)
headers = {"Authorization": f"{token['token_type']} {token['access_token']}"}

url = f"{url_path}/api_user/keys"
files = {"file": open("test_files/footers.docx", "rb")}
res = requests.post(url, files=files, headers=headers)
data = res.json()
print(data)

data["keys"]["hi"] = "Привет"
data["keys"]["buy"] = "Покеда"
data["keys"]["name"] = "Laplas"
data["keys"]["lastname"] = "Solomon"
data['keys']['data'] = "February"
data['keys']['satana'] = 'God'

data['tables']['cryptocurrency_tb'] = [
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

new_data = {'keys': data['keys'],
            #'tables': data['tables']
            }

filename = {"filename": "footers.docx",
            "newfilename": "shlyapa"}

url = f"{url_path}/api_user/render_link"
start_time = time.time()
res = requests.post(url, params=filename, json=new_data, headers=headers)
end_time = time.time()
execution_time = end_time - start_time
print("заполнение и конвертация (возврат через ссылку)")
print(execution_time)
print(res.json())

#             async with get_async_session() as session:
#                 await add_user_if_not_exists(session,
#                                              "admin",
#                                              "admin",
#                                              "nik_bogdanov2002@mail.ru",
#                                              "80865296a",
#                                              hashed.hash_password(ADMIN),
#                                              "admin")