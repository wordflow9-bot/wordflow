import random
import re
from typing import Tuple, Optional
from app.repositories.sqlite_repositories import SQLiteWordRepository
from app.core.models import UserWord

def _normalize_text(s: str) -> str: # нормализует строку (без знаков препинания и с одиночными пробелами)
    s = s.lower().strip()
    s = re.sub(r'[\W_]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s

class Trainer:
    def __init__(self, repo: SQLiteWordRepository):
        self.repo = repo

    def choose_word(self) -> Optional[UserWord]: # TODO change word picking strategy 
        words = self.repo.get_all()
        if not words:
            return None
        min_level = min(w.mastery_level() for w in words)
        candidates = [w for w in words if w.mastery_level() == min_level]
        return random.choice(candidates)
        # debug
        # return random.choice(words)

    def generate_question(self, mode: str = "word_to_translation") -> Optional[Tuple[int, str, str]]:
        w = self.choose_word()
        if w is None:
            return None
        if mode == "word_to_translation":
            return (w.id, w.word, w.translation)
        else:
            return (w.id, w.translation, w.word)

    def check_answer(self, word_id: int, user_answer: str) -> Tuple[bool, int]:
        w = self.repo.get_by_id(word_id)
        if w is None:
            return False, 0
        correct = _normalize_text(user_answer) == _normalize_text(w.translation)
        if correct:
            new_level = self.repo.adjust_mastery(word_id, 1) 
        else:
            new_level = self.repo.adjust_mastery(word_id, 0) 
        return correct, new_level
    
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
    