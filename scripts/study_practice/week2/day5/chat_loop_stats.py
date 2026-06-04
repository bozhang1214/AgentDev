import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = "你是一个有好的、专业的AI助手，请用中文回答用户的问题。"
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

total_input_tokens = 0
total_output_tokens = 0


def call_deepseek_with_history(user_input: str):
    """发送用户信息，获取助手回复，并更新消息历史和 token 计数"""
    global total_input_tokens, total_output_tokens

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            temperature=0.7
        )

        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})

        total_input_tokens += response.usage.prompt_tokens
        total_output_tokens += response.usage.completion_tokens

        return assistant_reply, response.usage

    except Exception as e:
        error_msg = f"API 调用失败：{e}"
        print(f"❌ {error_msg}")
        return None, None


def save_chat_history():
    """将完整的消息历史和统计数据保存到 JSON 文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = "data/chat_history"
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"chat_history_{timestamp}.json")

    data = {
        "saved_at": timestamp,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "messages": messages
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 对话历史已保存到: {filename}")
    print(
        f"📊 本次会话总计 token → 输入: {total_input_tokens}, 输出: {total_output_tokens}, 合计: {total_input_tokens + total_output_tokens}")


def main():
    print("=" * 60)
    print("🤖 多轮对话助手 (DeepSeek)")
    print("提示：输入 'exit' 或 'quit' 结束对话并保存历史")
    print("=" * 60)

    while True:
        user_input = input("\n👤 你: ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            print("正在保存对话历史...")
            save_chat_history()
            print("👋 再见！")
            break
        if not user_input:
            print("⚠️ 输入不能为空，请重新输入。")
            continue

        # 调用 API（自动更新历史）
        reply, usage = call_deepseek_with_history(user_input)
        if reply:
            print(f"\n🤖 助手: {reply}")
            # 打印本次调用的 token 明细（可选）
            if usage:
                print(
                    f"   [本次: 输入 {usage.prompt_tokens}, 输出 {usage.completion_tokens}]")
        else:
            print("⚠️ 未能获取回复，请检查网络或 API Key。")


if __name__ == "__main__":
    main()
