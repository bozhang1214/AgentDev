import json

with open("chat_history.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

user = loaded_data["user"]
messages = loaded_data["message"]

print(f"user: {user}")
for msg in messages:
    print(f"{msg['role']}: {msg['content']}")
