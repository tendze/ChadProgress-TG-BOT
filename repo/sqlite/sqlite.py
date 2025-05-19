import sqlite3
from repo.models.user import User
from repo.models.enum import UserRole

class ChadProgressDB:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    async def init_db(self):
        conn = sqlite3.connect(self.storage_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            jwt_token TEXT,
            role TEXT NOT NULL CHECK(role IN ('client', 'trainer')),
            photo_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    async def save_user(self, telegram_id: int, jwt_token: str, photo_id: str, role: str):
        conn = sqlite3.connect(self.storage_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users(telegram_id, jwt_token, photo_id, role) 
        VALUES(?, ?, ?, ?)
        """, (telegram_id, jwt_token, photo_id, role, ))
        conn.commit()
        conn.close() 

    async def get_user(self, telegram_id: int) -> User | None:
        conn = sqlite3.connect(self.storage_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT telegram_id, jwt_token, role, photo_id, created_at 
        FROM users 
        WHERE telegram_id = ?
        """, (telegram_id, ))

        row = cursor.fetchone()
        conn.close()

        if row:
            return User(
                telegram_id=row[0],
                jwt_token=row[1],
                role=row[2],
                photo_id=row[3],
                created_at=row[4]
            )
        return None
    
    async def exists(self, telegram_id: int) -> bool:
        conn = sqlite3.connect(self.storage_path)
        cursor = conn.cursor()
            
        cursor.execute("""
        SELECT EXISTS(
            SELECT 1 
            FROM users 
            WHERE telegram_id = ?
        )
        """, (telegram_id,))
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return bool(result)