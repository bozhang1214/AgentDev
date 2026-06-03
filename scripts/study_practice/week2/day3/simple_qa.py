import os
from backoff import constant
from openai import OpenAI
from dotenv import load_dotenv

ENV_KEY = "DEEPSEEK_API_KEY"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

load_dotenv()

api_key = os.getenv(ENV_KEY)
if not api_key:
    raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=BASE_URL
)


def call_deepseek(user_message: str):
    """调用 DeepSeek API，返回回复和 token 使用情况"""
    try:
        print("\n🤖 正在调用 DeepSeek API...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个友好的AI助手，请用中文回答用户的问题。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content

        prompt_tokens = response.usage.prompt_tokens
        completioin_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        return reply, prompt_tokens, completioin_tokens, total_tokens
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None, 0, 0, 0


def main():
    print("=" * 50)
    print("🤖 DeepSeek 命令行问答工具")
    print("输入您的问题，按回车获取回复")
    print("输入 'exit' 或 'quit' 退出")
    print("=" * 50)

    while True:
        user_input = input("\n 你：").strip()

        if user_input.lower() in ("exit", "quit"):
            print("👋 再见！")
            break

        if not user_input:
            print("⚠️ 输入不能为空，请重新输入。")
            continue

        reply, prompt_tokens, completion_tokens, total_tokens = call_deepseek(
            user_input)

        if reply:
            print(f"\n🤖 助手: {reply}")
            print("\n" + "-" * 40)
            print("📊 Token 统计:")
            print(f"   输入 token: {prompt_tokens}")
            print(f"   输出 token: {completion_tokens}")
            print(f"   总计 token: {total_tokens}")
            print("-" * 40)


if __name__ == "__main__":
    main()
