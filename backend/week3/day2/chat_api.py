import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI, api_key
from dotenv import load_dotenv

load_dotenv();
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    usage: dict

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "你是一个友好的AI助手，请用中文回答。"},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        usage = {
            "promp_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return ChatResponse(reply=reply, usage=usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "Chat API is running"}