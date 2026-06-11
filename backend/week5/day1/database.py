#database.py
import aiosqlite
import os

DB_PATH = "./data/conversations.db"

async def init_db():
    """初始化数据库表（如果不存在）"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tokens_used INTEGER DEFAULT 0,
                create_at TIMESTAMPT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON conversations(session_id)")
        await db.commit()

async def get_db():
    """返回数据库连接（用作依赖注入）"""
    async with aiosqlite.connect(DB_PATH) as db:
        # 设置 Row 工厂，返回字典风格的行
        db.row_factory = aiosqlite.Row
        yield db