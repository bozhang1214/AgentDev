"""
最小化 Function Calling 演示（模拟天气查询）
流程：
1. 定义 get_weather 工具的 JSON Schema
2. 用户提问 "北京今天天气怎么样？"
3. 模型返回 tool_calls
4. 模拟执行函数，返回结果
5. 再次调用模型，获得最终答案
"""

from ast import arguments
from email import message
import json
from json import tool
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请在 .env 中设置 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息（模拟）",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def mock_get_weather(location: str) -> str:
    return f"{location}当前天气：晴，温度 22°C，空气质量良好。"

def run_agent(user_message: str):
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手，可以使用工具查询天气。"},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.7
    )

    message = response.choices[0].message
    print(f"第一次响应：{message}")

    if message.tool_calls:
        messages.append(message.model_dump())
        for tool_call in message.tool_calls:
            if tool_call.function.name == "get_weather":
                arguments = json.loads(tool_call.function.arguments)
                location = arguments.get("location")
                weather_result = mock_get_weather(location)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": weather_result
                })
        
        second_response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            temperature=0.7
        )
        final_answer = second_response.choices[0].message.content
        return final_answer
    else:
        return message.content
    
if __name__ == "__main__":
    user_input = input("请输入问题：")
    answer = run_agent(user_input)
    print(f"\n最终回答：{answer}")