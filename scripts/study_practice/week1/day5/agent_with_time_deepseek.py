import asyncio
from datetime import datetime
import json
import os
import secrets
from urllib import response

from argon2 import Parameters
from dotenv import load_dotenv
from openai import APIError, AsyncOpenAI


load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量或在 .env 文件中提供")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间(北京时间/本地时间)",
            "Parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，例如 'Asia/Shanghai'，默认为本地时区",
                        "default": "Asia/Shanghai"
                    }
                }
            }
        }
    }
]


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """返回当前时间的字符串"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")


system_prompt = "你是一个智能助手，可以获取当前时间。当用户查询时间时，调用get_current_time 工具。"
messages = [
    {"role": "system", "content": system_prompt}
]

total_tokens = 0


async def call_agent(user_input: str):
    global total_tokens
    messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        # 第一次调用：可能返回 tool_calls
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        total_tokens += response.usage.total_tokens

        message = response.choices[0].message

        # 关键：先把 assistant 消息（可能含 tool_calls）加入历史
        messages.append(message)

        if message.tool_calls:
            # 处理每个 tool call
            for tool_call in message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    args = json.loads(tool_call.function.arguments)
                    timezone = args.get("timezone", "Asia/Shanghai")
                    result = get_current_time(timezone)
                    messages.append(
                        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                    )
            second_response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7
            )
            total_tokens += second_response.usage.total_tokens

            assistant_reply = second_response.choices[0].message.content
            messages.append({
                "role": "assistant", "content": assistant_reply
            })
            return assistant_reply
        else:
            # 没有工具调用，直接回复
            assistant_reply = message.content
            messages.append({
                "role": "assistant", "content": assistant_reply
            })
            return assistant_reply
    except APIError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Unknown Error: {e}"


async def main():
    print("🤖 智能 Agent (带时间工具) 已启动 | 输入 'exit' 退出")
    print("示例问题: '现在几点？' 或 '今天是几号？'")
    print("-" * 50)

    while True:
        user_input = input("\n 你：").strip()
        if user_input.lower() in ("exit", "quit"):
            print(f"\n📊 会话统计: 总 Token = {total_tokens}")
            print("👋 再见！")
            break
        if not user_input:
            continue

        print("思考中...")
        reply = await call_agent(user_input)
        print(f"\n🤖 助手: {reply}")
        print(f"📈 当前累计 Token: {total_tokens}")

if __name__ == "__main__":
    asyncio.run(main())
