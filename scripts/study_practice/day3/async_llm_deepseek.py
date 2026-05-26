import asyncio
import time
import os
from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError, APITimeoutError
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError(
        "No API key found. Please set DEEPSEEK_API_KEY in your environment variables.")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
)


async def call_llm_async(user_message: str):
    """异步请求中调用 DeepSeek LLM 并返回回复和 token 信息"""
    try:
        print("异步请求中...")
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": user_message}
            ],
            timeout=10,  # 设置请求超时时间为 10 秒
        )
        reply = response.choices[0].message.content
        usage = response.usage
        return reply, usage
    except APITimeoutError:
        print("请求超时，请稍后再试。")
    except APIConnectionError:
        print("网络连接错误，请检查您的网络连接。")
    except RateLimitError:
        print("请求过于频繁，请稍后再试。")
    except APIError as e:
        print(f"API 错误: {e}")
    return None, None


async def main():
    user_message = "你好，请用一句话介绍什么事异步编程。"

    print(f"输入信息： {user_message}")
    start = time.time()
    reply, usage = await call_llm_async(user_message)
    elapsed = time.time() - start

    if reply:
        print(f"模型回复：\n{reply}")
        if usage:
            print(f"\n[Token 详细统计]")
            print(f"输入 token (API 返回): {usage.prompt_tokens}")
            print(f"输出 token (API 返回): {usage.completion_tokens}")
            print(f"总计 token (API 返回): {usage.total_tokens}")
        print(f"\n请求耗时: {elapsed:.2f} 秒")
    else:
        print("未能获取模型回复。")

if __name__ == "__main__":
    asyncio.run(main())
