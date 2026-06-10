import requests
import json

BASE_URL = "http://localhost:8001"

def test_weather_agent():
    session_id = "test_session_001"
    question = "北京今天天气怎么样？"

    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": question, "session_id": session_id}
    )
    data = response.json()
    print(f"问题: {question}")
    print(f"回复: {data['reply']}")
    print(f"工具调用: {data.get('tool_called', False)}")
    print(f"Token 使用: {data['usage']}")

    question2 = "那上海呢？"
    response2 = requests.post(
        f"{BASE_URL}/chat",
        json={"message": question2, "session_id": session_id}
    )
    data2 = response2.json()
    print(f"\n问题: {question2}")
    print(f"回复: {data2['reply']}")
    print(f"工具调用: {data2.get('tool_called', False)}")

if __name__ == "__main__":
    test_weather_agent()