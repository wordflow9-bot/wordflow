from dataclasses import dataclass
from typing import Optional
# from datetime import datetime

@dataclass
class Word:
    id: Optional[int]
    word: str
    translation: str
    mastery_level: int = 0
    # created_at: datetime = None
    # updated_at: datetime = None
