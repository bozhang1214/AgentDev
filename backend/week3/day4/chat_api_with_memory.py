from email import message
import os
import uuid
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

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
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    usage: dict

app = FastAPI(title="带记忆的聊天API")

def get_or_create_session(session_id: Optional[str] = None) -> tuple[str, list]:
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
            temperature=0.7
        )

        reply = response.choices[0].message.content
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        sessions[sess_id].append({"role": "user", "content": request.message})
        sessions[sess_id].append({"role": "assistant", "content": reply})
        return ChatResponse(
            reply=reply,
            session_id=sess_id,
            usage=usage
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
