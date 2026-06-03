import asyncio
import json
import os
from datetime import datetime
from openai import AsyncOpenAI, APIError
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")

# DeepSeek API 兼容 OpenAI 接口， 需指定 base_url
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

SYSTEM_PROMPT = "你是一个友好、专业的AI助手，请用中文回答用户的问题。"
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

total_tokens_used = 0


async def get_llm_response(user_input: str) -> str:
    """调用 DeepSeek API 并返回回复，同时更新 message 和 token 累计"""
    global total_tokens_used
    messages.append({"role": "user", "content": user_input})

    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7
        )
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        total_tokens_used += response.usage.total_tokens
        return assistant_reply
    except APIError as e:
        return f"! API Error {e}"
    except Exception as e:
        return f"! Unknown Error: {e}"


# def save_history():
#     """将对话历史保存到 JSON 文件"""
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"data/chat_history/chat_history_{timestamp}.json"
#     data = {
#         "saved_at": timestamp,
#         "total_tokens_used": total_tokens_used,
#         "messages": messages
#     }
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#     print(f"\n conversation history save to: {filename}")
#     print(f"used token of this conversation: {total_tokens_used}")

def save_history():
    """将对话历史保存到 JSON 文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = "data/chat_history"
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"chat_history_{timestamp}.json")
    data = {
        "saved_at": timestamp,
        "total_tokens_used": total_tokens_used,
        "messages": messages
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n conversation history save to: {filename}")
    print(f"used token of this conversation: {total_tokens_used}")


async def main():
    print("多轮对话机器人已经启动（输入 'exit' 或者 'quit' 退出")
    print("=" * 50)

    while True:
        user_input = input("\n 你： ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("再见！正在保存历史...")
            save_history()
            break

        if not user_input:
            print("输入不能为空，请重新输入。")
            continue

        print("思考中...")
        reply = await get_llm_response(user_input)
        print(f" 助手：{reply}")
        print(f" 当前累计 token：{total_tokens_used}")

if __name__ == "__main__":
    asyncio.run(main())
