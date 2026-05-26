# AgentDev 项目文件与目录说明

本文档描述 AgentDev 工程的主要文件与目录结构，帮助快速了解项目布局与各部分职责。

## 概览

- 项目根目录包含容器与部署配置、后端服务代码、前端应用以及数据与脚本等。

## 目录树

```
AgentDev/
├── .devcontainer/          # 开发容器配置
├── .github/                # GitHub CI/CD 流程配置
├── backend/                # 后端 Python 服务代码
│   ├── __init__.py         # Python 包初始化
│   ├── main.py             # FastAPI 服务入口
│   └── s1-w1/              # 示例/子服务目录
│       └── d1/
│           ├── agent/      # Agent 逻辑实现目录
│           └── web/        # Web/API 相关目录
├── config/                 # 配置与环境示例
│   └── .env.example        # 环境变量示例文件
├── data/                   # 项目运行或开发所需数据资源
├── docs/                   # 文档说明与 Agent 说明文件
│   ├── AGENTS.md
│   └── CLAUDE.md
├── frontend/               # 前端 Next.js 应用
│   ├── app/                # Next.js 页面与布局代码
│   ├── public/             # 静态资源
│   └── package.json        # 前端依赖与脚本
├── notebooks/              # Jupyter 笔记本、实验与分析
├── scripts/                # 辅助脚本与自动化工具
├── tests/                  # 自动化测试代码
├── Dockerfile              # 容器镜像构建定义
├── docker-compose.yml      # 服务编排配置
├── requirements.txt        # Python 后端依赖清单
├── README.md               # 项目快速启动与说明
└── PROJECT_STRUCTURE.md    # 工程结构说明
```

## 顶层文件

- `docker-compose.yml`：用于组合和运行多个 Docker 服务的编排文件。
- `Dockerfile`：定义项目容器镜像构建流程（通常用于后端或服务镜像）。
- `requirements.txt`：Python 依赖清单，用于创建虚拟环境并安装所需包。

## 目录说明

- `backend/`（原 `app/`）
  - 后端 Python 服务主目录（已从 `app/` 重命名以避免与前端 `app/` 混淆）。
  - `__init__.py`：Python 包初始化文件。
  - `main.py`：后端应用入口（包含 FastAPI 服务启动代码）。
  - `s1-w1/`：示例或子服务目录（命名可能代表场景/工作流）。
    - `d1/`
      - `agent/`：agent 相关实现代码（策略、任务逻辑等）。
      - `web/`：与 agent 相关的 web/前端或 API 层实现（如果存在）。

- `data/`
  - 项目运行或开发用到的静态数据、示例文件或模型资源存放位置。

- `frontend/`
  - 前端 Next.js/React 项目目录。
  - `AGENTS.md`、`CLAUDE.md`：关于不同 agent 或集成的说明文档。
  - `package.json`：前端依赖与运行脚本定义。
  - `app/`：Next.js 应用源码（包括 `page.tsx`, `layout.tsx`, 全局样式等）。
  - `public/`：静态资源（图片、favicon 等）。
  - 其它配置文件：`tsconfig.json`、`next.config.ts`、`eslint.config.mjs`、`postcss.config.mjs` 等。

- `notebooks/`
  - Jupyter 笔记本，用于实验、分析、演示或模型调试。

- `scripts/`
  - 项目相关的辅助脚本（部署、迁移、数据处理等自动化脚本）。

## 使用与运行（简要）

- 安装后端依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- 启动 Docker 服务（若使用）：

```bash
docker-compose up --build
```

- 运行前端（进入 `frontend/`）：

```bash
cd frontend
npm install
npm run dev
```

## 开发建议

- 后端与前端分离开发，使用容器化保持环境一致性。
- 将 agent 逻辑放入 `backend/.../agent/` 子目录，便于单元测试与复用。
- 在 `docs/AGENTS.md` 中维护各 Agent 的使用说明与集成细节。

## 联系与维护

如需更新本说明，请编辑本文件 `PROJECT_STRUCTURE.md` 并提交合并请求，或联系项目维护者补充细节。
