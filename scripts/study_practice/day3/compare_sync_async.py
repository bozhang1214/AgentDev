import asyncio
import time
import os
from typing import Any
from openai import OpenAI, AsyncOpenAI
from openai import APIError, APIConnectionError, RateLimitError, APITimeoutError
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError(
        "No API key found. Please set DEEPSEEK_API_KEY in your environment variables.")

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

QUESTIONS = [
    "用一句话解释什么是递归。",
    "用一句话解释什么是闭包。",
    "用一句话解释什么是异步编程。"
]

# ---- sync ---
sync_client = OpenAI(api_key=api_key, base_url=BASE_URL)


def call_llm_sync(user_message: str) -> str | Any:
    """同步请求中调用 DeepSeek LLM 并返回回复和 token 信息"""
    try:
        print("同步请求中...")
        response = sync_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": user_message}
            ],
            timeout=10.0,  # 设置请求超时时间为 10 秒
        )
        return response.choices[0].message.content
    except (APIConnectionError, RateLimitError, APITimeoutError, APIError) as e:
        print(f"❌ 同步调用出错: {e}")
        return None


def sync_serial():
    """同步串行执行三个请求"""
    print("\n 同步串行执行开始...")
    start = time.time()
    results = []
    for idx, q in enumerate(QUESTIONS, 1):
        print(f" 发送请求 {idx}...")
        answer = call_llm_sync(q)
        results.append(answer)
        if answer:
            print(f" 收到回复 {idx}: {answer[:50]}...")
    elapsed = time.time() - start
    print(f"同步串行执行完成，耗时: {elapsed:.2f} 秒")
    return elapsed, results


# ---- async ---
async_client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)


async def call_llm_async(question: str) -> str | Any:
    """异步调用，返回回复内容"""
    try:
        response = await async_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
            timeout=10.0,
        )
        return response.choices[0].message.content
    except (APIConnectionError, RateLimitError, APITimeoutError, APIError) as e:
        print(f"❌ 异步调用出错: {e}")
        return None


async def async_concurrent():
    """异步并发执行三个请求"""
    print("\n 异步并发执行开始...")
    start = time.time()
    tasks = [call_llm_async(q) for q in QUESTIONS]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    for idx, answer in enumerate(results, 1):
        if answer:
            print(f" 收到回复 {idx}: {answer[:50]}...")
    print(f"异步并发执行完成，耗时: {elapsed:.2f} 秒")
    return elapsed, results


async def main():
    print("=" * 50)
    print("性能对比：三个请求（同步串行 vs 异步并发）")
    print("=" * 50)

    sync_time, sync_results = sync_serial()
    async_time, async_results = await async_concurrent()

    # 对比结果
    print("\n性能对比结果：")
    print(f"同步串行总耗时: {sync_time:.2f} 秒")
    print(f"异步并发总耗时: {async_time:.2f} 秒")
    if async_time > 0:
        speedup = sync_time / async_time
        print(f"异步并发相较于同步串行的加速比: {speedup:.2f}x")
    else:
        print("异步并发耗时为 0，无法计算加速比。")

if __name__ == "__main__":
    asyncio.run(main())
