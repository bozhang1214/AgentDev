# 个人工具页 - 待办清单 + AI 聊天助手

这是一个结合了待办管理和 AI 对话的 React + FastAPI 全栈应用。

## 功能

- 待办清单：添加、删除、标记完成，数据自动保存到 localStorage
- AI 助手：多轮对话，支持会话记忆，显示 token 消耗

## 技术栈

- 前端：React (Vite) + 原生 CSS
- 后端：FastAPI + DeepSeek API + 内存存储

## 如何运行

### 后端

1. 安装依赖：`pip install fastapi uvicorn openai python-dotenv`
2. 在项目根目录创建 `.env` 文件，填入 `DEEPSEEK_API_KEY=你的密钥`
3. 运行：`uvicorn chat_api_with_memory:app --reload --port 8000`
4. 端口被占的话可以调整为8001或递加尝试

### 前端

1. `npm install`
2. `npm run dev`
3. 访问 `http://localhost:5173`

## 演示截图

![alt text](image.png)

## 学习笔记
