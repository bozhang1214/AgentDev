# backend/main.py
import os
import json
import uuid
from contextlib import asynccontextmanager
from typing import List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import aiosqlite

from database import init_db, get_db, save_message, get_messages

# ---------- 加载环境变量 ----------
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("请在 .env 中设置 DEEPSEEK_API_KEY")

# ---------- 初始化 OpenAI 客户端（兼容 DeepSeek）----------
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ---------- 数据模型 ----------
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    usage: dict
    tool_called: bool = False

# ---------- 系统提示 ----------
SYSTEM_PROMPT = "你是一个友好、专业的 AI 助手，请用中文回答用户的问题。"

# ---------- 定义天气工具（Function Calling）----------
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
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
tools = [weather_tool]

# ---------- 模拟天气函数（实际可调用真实 API）----------
async def get_weather(location: str) -> str:
    """模拟天气查询，实际应调用 OpenWeatherMap 等 API"""
    # 这里可以替换为真实的 httpx 异步请求
    return f"{location}当前天气：晴，温度 22°C，空气质量良好。"

# ---------- FastAPI 生命周期管理 ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    print("数据库初始化完成")
    yield
    # 关闭时清理（如果有需要关闭的连接，可在此处添加）
    print("应用关闭")

app = FastAPI(lifespan=lifespan)

# 配置 CORS（允许前端开发服务器跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 辅助函数：执行工具调用 ----------
async def execute_tool_calls(tool_calls: List[Any]) -> List[Dict[str, Any]]:
    """执行 tool_calls 并返回 tool 角色的消息列表"""
    tool_messages = []
    for tool_call in tool_calls:
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            location = args.get("location")
            weather_result = await get_weather(location)
            tool_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": weather_result
            })
    return tool_messages

# ---------- 核心聊天端点 ----------
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: aiosqlite.Connection = Depends(get_db)):
    # 确定 session_id
    sess_id = request.session_id or str(uuid.uuid4())

    # 1. 从数据库加载最近的历史消息（最多 20 条，控制 token 消耗）
    history = await get_messages(db, sess_id, limit=20)
    # 转换为 OpenAI 消息格式
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    messages.append({"role": "user", "content": request.message})

    # 保存用户消息到数据库（先保存，后续若工具调用失败也可追溯）
    await save_message(db, sess_id, "user", request.message, 0)

    total_prompt_tokens = 0
    total_completion_tokens = 0
    tool_called = False

    try:
        # 第一次调用：可能返回 tool_calls
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        total_prompt_tokens += response.usage.prompt_tokens
        total_completion_tokens += response.usage.completion_tokens

        assistant_message = response.choices[0].message

        # 检查是否需要调用工具
        if assistant_message.tool_calls:
            tool_called = True
            # 将助手的 tool_calls 响应追加到对话中
            messages.append(assistant_message.model_dump())  # 或手动构造字典

            # 执行工具调用
            tool_messages = await execute_tool_calls(assistant_message.tool_calls)
            for tm in tool_messages:
                messages.append(tm)

            # 第二次调用：将工具结果发给模型生成最终答案
            second_response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=messages,
                temperature=0.7
            )
            total_prompt_tokens += second_response.usage.prompt_tokens
            total_completion_tokens += second_response.usage.completion_tokens
            final_reply = second_response.choices[0].message.content
        else:
            # 没有工具调用，直接使用第一次回复
            final_reply = assistant_message.content

        # 保存助手回复到数据库
        await save_message(db, sess_id, "assistant", final_reply, total_completion_tokens)

        usage = {
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens
        }

        return ChatResponse(
            reply=final_reply,
            session_id=sess_id,
            usage=usage,
            tool_called=tool_called
        )

    except Exception as e:
        # 异常时可选：将错误信息保存为助手消息（便于调试）
        error_msg = f"处理请求时出错：{str(e)}"
        await save_message(db, sess_id, "assistant", error_msg, 0)
        raise HTTPException(status_code=500, detail=str(e))

# ---------- 健康检查端点 ----------
@app.get("/health")
async def health():
    return {"status": "ok"}