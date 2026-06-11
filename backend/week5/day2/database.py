# database.py
import aiosqlite
import os

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 将数据库文件放在当前文件所在目录下的 data 子目录中
DB_PATH = os.path.join(BASE_DIR, "data", "conversations.db")
TABLE_NAME = "conversations"

async def init_db():
    """初始化数据库表（应用启动时调用一次）"""
    # 确保数据库文件所在的目录存在
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tokens_used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON conversations(session_id)")
        await db.commit()

async def get_db():
    """依赖注入：提供数据库连接，请求结束后自动关闭"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def save_message(db: aiosqlite.Connection, session_id: str, role: str, content: str, tokens_uses: int = 0):
    """保存一条消息到数据库"""
    await db.execute(
        "INSERT INTO conversations (session_id, role, content, tokens_used) VALUES (?, ?, ?, ?)",
        (session_id, role, content, tokens_uses)
    )
    await db.commit()

async def get_messages(db: aiosqlite.Connection, session_id: str, limit: int = 20):
    """获取某个会话最近的消息（按时间升序）"""
    cursor = await db.execute(
        "SELECT role, content, tokens_used, created_at FROM conversations WHERE session_id = ? ORDER BY created_at ASC LIMIT ?", (session_id, limit)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

async def delete_session(db: aiosqlite.Connection, session_id: str):
    """删除整个会话的历史"""
    await db.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
    await db.commit()

