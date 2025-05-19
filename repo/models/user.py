from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    telegram_id: int
    role: str
    photo_id: str
    jwt_token: Optional[str] = None
    created_at: Optional[str] = None