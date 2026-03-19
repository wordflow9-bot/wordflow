from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional
from enum import auto, Enum
# from datetime import datetime


@dataclass_json
@dataclass
class Word:
    ru: str
    en: str


@dataclass
class Button:
    message_id: int
    metadata: Optional[Word] = None


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
    word: Word
    total_cnt: int = 0
    correct_cnt: int = 0
    # mastery_level: int = 0

    def mastery_level(self) -> int:  # TODO: переделать на нецелочисленную арифметику
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


class SessionType(Enum):  # какому микросервису _ принадлежит_тип
    main_menu = auto()
    database_add_word = auto()
    database_add_word_choose_translation = auto()
    translator = auto()
    train_check_answer = auto()
    train_end = auto()


@dataclass_json
@dataclass
class Session:
    session_type: SessionType
    crutch: Optional[UserWord] = None


