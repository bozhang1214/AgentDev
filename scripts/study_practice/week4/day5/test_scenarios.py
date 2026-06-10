import glob

import requests
import time

BASE_URL = "http://localhost:8001"
SESSION_ID = None

def ask(question):
    global SESSION_ID
    payload = {"message": question}
    if SESSION_ID:
        payload["session_id"] = SESSION_ID
    

    resp = requests.post(f"{BASE_URL}/chat", json=payload)
    data = resp.json()
    SESSION_ID = data["session_id"]
    print(f"Q: {question}")
    print(f"A: {data['reply']}")
    print(f"Tool called: {data.get('tool_called')}")
    print(f"Tokens: {data['usage']['total_tokens']}\n")
    return data

if __name__ == "__main__":
    # 场景1: 单一城市
    ask("北京今天天气怎么样？")
    
    # 场景2: 多城市比较（可能需要多次工具调用）
    ask("上海和杭州哪个更暖和？")
    
    # 场景3: 基于天气的推理
    ask("今天适合出门吗？")
    
    # 场景4: 连续对话记忆（检验缓存是否影响记忆）
    ask("那明天呢？")  # 注意：模型可能没有明天的数据，会合理回答