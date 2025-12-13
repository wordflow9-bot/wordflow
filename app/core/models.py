from dataclasses import dataclass
from typing import Optional
# from datetime import datetime

@dataclass
class UserWord:
    user_id: Optional[int]
    word_id: Optional[int]
    word: str
    translation: str
    total_cnt: int = 0
    correct_cnt: int = 0
    mastery_level: int = 0
    # created_at: datetime = None
    # updated_at: datetime = None

