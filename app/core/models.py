from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional
# from datetime import datetime


@dataclass
class User:
    id: Optional[int]
    telegram_id: str
    # created_at: Optional[datetime] = None


@dataclass_json
@dataclass
class UserWord:
    id: Optional[int]
    user_id: Optional[int]
    # word_id: Optional[int]
    word: str
    translation: str
    total_cnt: int = 0
    correct_cnt: int = 0
    # mastery_level: int = 0
    def mastery_level(self) -> int: # TODO: переделать на нецелочисленную арифметику
        if self.total_cnt != 0:
            return round(self.correct_cnt / self.total_cnt * 100)
        return 0
    # created_at: datetime = None
    # updated_at: datetime = None


@dataclass
class TrainingSession:
    id: Optional[int]
    user_id: int
    user_word_id: int
    user_answer: str
    is_correct: bool
    # created_at: Optional[datetime] = None


@dataclass_json
@dataclass
class Session:
    # session_id: Optional[int] нигде пока неиспользуется тк ключи user_id
    # user_id: Optional[int] кажется также не требуется
    session_type: str
    crutch: Optional[UserWord] = None




