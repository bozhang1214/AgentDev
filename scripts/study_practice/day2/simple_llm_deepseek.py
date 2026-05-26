import os
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("Using OpenAI API key from environment variable.")
    else:
        raise ValueError(
            "No API key found. Please set DEEPSEEK_API_KEY or OPENAI_API_KEY in your environment variables.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
)

user_message = "你好，请用一句话介绍什么事异步编程。"

start = time.time()

print("正在调用 DeepSeek 模型...")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": user_message}
    ],
    temperature=0.7,
)

assistant_reply = response.choices[0].message.content
print("DeepSeek 模型回复:", assistant_reply)

input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens
elapsed = time.time() - start

print(f"\n[Token 详细统计]")
print(f"输入 token (API 返回): {input_tokens}")
print(f"输出 token (API 返回): {output_tokens}")
print(f"总计 token (API 返回): {total_tokens}")
print(f"模型调用耗时(同步)：{elapsed:.2f} 秒")
