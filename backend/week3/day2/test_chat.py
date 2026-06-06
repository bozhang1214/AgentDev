import requests

url = "http://localhost:8001/chat"
payload = {"message": "详细解释一下什么事React"}
response = requests.post(url, json=payload)
print(response.json())