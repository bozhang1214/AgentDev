import os
import json
import re
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

PRICE_INPUT = 1.0
PRICE_OUTPUT = 2.0
SYSTEM_PROMPT = "你是一个有好的、专业的AI助手，请用中文回答用户的问题。"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

total_input_tokens = 0
total_output_tokens = 0


def get_current_time():
    """返回当前时间的字符串"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")


def is_time_query(user_input: str) -> bool:
    """简单正则判断是否查询时间（不区分大小写）"""
    patterns = [
        r"现在几点了",
        r"当前时间",
        r"现在时间",
        r"几点了",
        r"现在几点",
        r"what time",
        r"current time",
        r"时间"
    ]
    for pat in patterns:
        if re.search(pat, user_input, re.IGNORECASE):
            return True
    return False


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


def compute_cost(input_tokens, output_tokens):
    """计算单次或累积成本"""
    cost = (input_tokens / 1_000_000) * PRICE_INPUT + \
        (output_tokens / 1_000_000) * PRICE_OUTPUT
    return cost


def print_stats(prefix="本次", input_t=None, output_t=None):
    """打印 token 和成本统计，如果传入具体数值则打印单次，否则打印累计"""
    if input_t is not None and output_t is not None:
        cost = compute_cost(input_t, output_t)
        print(
            f"    [{prefix} Token] 输入：{input_t}, 输出：{output_t}, 成本：{cost:.6f} 元")
    else:
        total_t = total_input_tokens + total_output_tokens
        cost = compute_cost(total_input_tokens, total_output_tokens)
        print("\n📊 会话总统计:")
        print(f"   总输入 token: {total_input_tokens}")
        print(f"   总输出 token: {total_output_tokens}")
        print(f"   总 token: {total_t}")
        print(f"   预估总成本: {cost:.6f} 元")


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
    print("提示：输入 'exit'、'q' 或 'quit' 结束对话并保存历史")
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

        if is_time_query(user_input):
            time_str = get_current_time()
            print(f"\n🤖 助手: 当前时间是 {time_str}")
            continue

        # 调用 API（自动更新历史）
        reply, usage = call_deepseek_with_history(user_input)
        if reply:
            print(f"\n🤖 助手: {reply}")
            # 打印本次调用的 token 明细（可选）
            if usage:
                print_stats("本次", usage.prompt_tokens, usage.completion_tokens)
                # 显示累计成本（可选）
                cum_cost = compute_cost(
                    total_input_tokens, total_output_tokens)
                print(f"   [累计] 总成本: {cum_cost:.6f} 元")
        else:
            print("⚠️ 未能获取回复，请检查网络或 API Key。")


if __name__ == "__main__":
    main()
