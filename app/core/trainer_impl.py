import random
import re
from typing import Tuple, Optional
from app.repositories.sqlite_repositories import SQLiteWordRepository
from app.core.models import Word, UserWord


def _normalize_text(s: str) -> str:  # нормализует строку (без знаков препинания и с одиночными пробелами)
    s = s.lower().strip()
    s = re.sub(r'[\W_]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s


class Trainer:
    def __init__(self, repo: SQLiteWordRepository):
        self.repo = repo

    def choose_word(self, user_id: int) -> Optional[UserWord]:
        words = self.repo.get_all(user_id)
        if not words:
            return None
        return random.choices(words, weights=[(101 - word.mastery_level()) ** 0.1 for word in words])[0]

    def generate_question(self, user_id: int, mode: str = "ru") -> Optional[Word]: # TODO: переделать, НЕРАБОТАЕТ
        w = self.choose_word(user_id)
        if w is None:
            return None
        if mode == "ru":
            w.word.en = ""
        else:
            w.word.ru = ""
        return w.word

    def check_answer(self, user_id: int, word: Word) -> Optional[int]:  # i_level | wrong
        word.ru = _normalize_text(word.ru)
        word.en = _normalize_text(word.en)
        word_id = self.repo.get_word_id(user_id, word)
        if word_id is None:
            return None
        new_level = self.repo.adjust_mastery(word_id, 1)
        return new_level
    
    #debug
    # def check_answer(self, word_id: int, correct) -> Tuple[bool, int]:
    #     w = self.repo.get_by_id(word_id)
    #     if w is None:
    #         return False, 0
    #     if correct:
    #         new_level = self.repo.adjust_mastery(word_id, 1) 
    #     else:
    #         new_level = self.repo.adjust_mastery(word_id, 0) 
    #     return correct, new_level
