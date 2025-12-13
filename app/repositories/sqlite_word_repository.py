import sqlite3
from typing import List, Optional
from dataclasses import dataclass
from app.core.models import UserWord


class SQLiteWordRepository:
    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path) # TODO: что делает detect_types=sqlite3.PARSE_DECLTYPES)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    word TEXT, 
                    translation TEXT, 
                    total_cnt INTEGER, 
                    correct_cnt INTEGER)""")
            conn.commit()

    def add_word(self, user_id: int, word: str, translation: str) -> UserWord:
        with self._get_conn() as conn:
            cur = conn.cursor().execute(
                "INSERT INTO words (user_id, word, translation, total_cnt, correct_cnt) VALUES (?, ?, ?, 0, 0)",
                (user_id, word, translation)
            )
            id_ = cur.lastrowid
            return self.get_by_id(id_)

    def get_all(self) -> List[UserWord]:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("SELECT * FROM words")
            rows = cur.fetchall()
            return [UserWord(*row) for row in rows]

    def get_by_id(self, word_id: int) -> Optional[UserWord]:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("SELECT * FROM words WHERE id = ?", (word_id,))
            row = cur.fetchone()
            return UserWord(*row) if row else None

    def update_word(self, id_: int, word: Optional[str], translation: Optional[str]) -> bool:
        # TODO: Реализовать update с условной подстановкой полей
        pass

    def delete_word(self, id_: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("DELETE FROM words WHERE id = ?", (id_,))
            conn.commit()
            # return cur.rowcount > 0
            return 1

    def adjust_mastery(self, id_: int, delta_correct_cnt: int = 1, delta_total_cnt: int = 1) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("UPDATE words SET total_cnt = total_cnt + ?, correct_cnt = correct_cnt + ? WHERE id = ?", (delta_total_cnt, delta_correct_cnt, id_))
            conn.commit()
            # return self.get_by_id(id_).mastery_level
            return 1

    def clear(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""DELETE FROM words""")
            conn.commit()


# debug
# sq = SQLiteWordRepository()
# sq.clear()
# sq.add_word(100, 'orlov', 'gay')
# sq.add_word(100, 'orlov1', 'gay1')
# sq.add_word(100, 'orlov2', 'gay2')
# sq.add_word(100, 'orlov3', 'gay3')
# print(sq.get_by_id(20))
# sq.adjust_mastery(20, 1)
# sq.adjust_mastery(21, 0)
# print(*sq.get_all(), sep='\n')
# sq.adjust_mastery(1)
