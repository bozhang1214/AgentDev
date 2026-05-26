# backend/main.py
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（如果你在 docker-compose 中已经通过 env_file 加载，此行可省略）
load_dotenv()

# 创建 FastAPI 应用实例
app = FastAPI(
    # title="AI Agent API",
    # description="一个基于 CrewAI/LangChain 的智能 Agent 服务",
    # version="1.0.0",
)

# ---------- 请求/响应数据模型 ----------


class ChatRequest(BaseModel):
    question: str = Field(..., description="用户提出的问题", example="什么是 Docker？")
    user_id: Optional[str] = Field(None, description="可选用户ID，用于区分会话")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Agent 的回答")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度（0-1）")

# ---------- 模拟 Agent 逻辑（后面替换为真实的 CrewAI/LangChain 调用）----------


def run_agent(question: str) -> tuple[str, float]:
    """
    执行 Agent 逻辑。
    返回 (回答文本, 置信度)
    """
    # TODO: 在这里集成你的 CrewAI 或 LangChain 流程
    # 示例：调用 OpenAI（需设置 OPENAI_API_KEY）
    # from langchain_openai import ChatOpenAI
    # from langchain.schema import HumanMessage
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # response = llm.invoke([HumanMessage(content=question)])
    # return response.content, 0.9

    # 临时模拟回答（以便测试）
    answer = f"【模拟回答】您的问题是：“{question}”。这是来自 Agent 的测试响应。"
    confidence = 0.95
    return answer, confidence

# ---------- API 路由 ----------


@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查接口，用于确认服务是否运行正常"""
    return {"status": "ok", "message": "Agent 服务正在运行"}


@app.post("/agent/chat", response_model=ChatResponse, tags=["Agent"])
async def chat_endpoint(request: ChatRequest):
    """
    与 Agent 对话的端点。
    接收用户问题，返回 Agent 的答案和置信度。
    """
    try:
        answer, conf = run_agent(request.question)
        return ChatResponse(answer=answer, confidence=conf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 处理失败: {str(e)}")

# ---------- 可选：启动时加载模型等资源 ----------


@app.on_event("startup")
async def startup_event():
    # 这里可以执行初始化代码，例如加载向量数据库、模型等
    print("Agent 服务启动中...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Agent 服务关闭...")


@app.get("/ping")
def ping():
    return {"status": "ok", "container": "agent-dev"}
