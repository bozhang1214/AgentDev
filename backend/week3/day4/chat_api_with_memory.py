from datetime import datetime
from email import message
import os
import uuid
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse
from tools.weather_service import get_weather

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"
MAX_HISTORY_LENGTH = 40

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=BASE_URL
)

sessions = {}

SYSTEM_PROMPT = "你是一个友好的、专业的 AI 助手，请用中文回答用的问题。"

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    usage: dict

app = FastAPI(title="带记忆的聊天API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_or_create_session(session_id: str | None = None) :
    """获取会话历史，若不存在则创建新会话"""
    if session_id is None or session_id not in sessions:
        new_id = str(uuid.uuid4())
        sessions[new_id] = []
        return new_id, []
    else:
        return session_id, sessions[session_id]
    
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    sess_id, history = get_or_create_session(request.session_id)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            timeout=10.0
        )

        reply = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        sessions[sess_id].append({"role": "user", "content": request.message})
        sessions[sess_id].append({"role": "assistant", "content": reply})
        if len(sessions[sess_id]) > MAX_HISTORY_LENGTH:
            sessions[sess_id] = sessions[sess_id][-MAX_HISTORY_LENGTH]
        return ChatResponse(
            reply=reply,
            session_id=sess_id,
            usage=usage
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/history/{session_id}")
def get_history(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": sessions[session_id]}

@app.get("/")
def root():
    return {"message": "Chat API with memory is running", "active_sessions": len(sessions)}

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """删除指定会话的历史(释放内存)"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not fount!")

todo_storage = {}

class TodoItem(BaseModel):
    id: int
    text: str
    completed: bool = False

class TodoCreate(BaseModel):
    session_id: str
    text:str

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate):
    if todo.session_id not in todo_storage:
        todo_storage[todo.session_id] = []

    new_id = int(datetime.now().timestamp() * 1000)
    new_todo = {"id": new_id, "text": todo.text, "completed": False}
    todo_storage[todo.session_id].append(new_todo)
    return new_todo

@app.get("/todos/{session_id}")
def get_todos(session_id: str):
    return todo_storage.get(session_id, [])

@app.delete("/todos/{session_id}/{todo_id}")
def delete_todo(session_id: str, todo_id: int):
    if session_id in todo_storage:
        todo_storage[session_id] = [t for t in todo_storage[session_id] if t["id"] != todo_id]
        return {"message": "deleted"}
    raise HTTPException(status_code=404, detail="Session not found")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误：{str(exc)}"}
    )

@app.get("/weather")
async def weather_endpoint(location: str = Query(..., description="城市名称，如Beijing")):
    """
    获取指定城市的当前天气
    示例：GET /weather?location=Beijing
    """
    weather_info = await get_weather(location)
    print(f"weather_info: {weather_info}")
    return {"location": location, "weather": weather_info}