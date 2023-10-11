import requests
import json


file = {'file': open("test_files/typical.docx", 'rb')}

data = {"id_user": "user1"}

# res = requests.post("http://81.200.156.178:7777/verification", files=file, data=data)
res = requests.post("http://81.200.156.178:7777/verification", files=file, data=data)

tag = res.json()

print(tag)

tag["tags"]["Browser"] = "Gooogle"
tag["tags"]["Version"] = "0.0.0.0.1"
tag["tags"]["IP"] = "0.0.0.127"
tag["tags"]["Location"] = "Russia"
tag["tags"]["Created"] = "Konstantine"

res = requests.post("http://81.200.156.178:7777/placeholder", json=json.dumps(tag))

with open("out_files/out.pdf", "wb") as code:
    code.write(res.content)