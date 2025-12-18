import sqlite3
from typing import List, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from app.core.models import UserWord, Session


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
            lvl = self.get_by_id(id_).mastery_level()
            return lvl

    def clear(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""DELETE FROM words""")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='words';")
            conn.commit()


class SQLiteSessionRepository:
    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)  # TODO: что делает detect_types=sqlite3.PARSE_DECLTYPES)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""CREATE TABLE IF NOT EXISTS sessions(session_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER UNIQUE,
                    session_json TEXT
                    )""")
            conn.commit()

    def get_session(self, user_id) -> Optional[Session]:
        with self._get_conn() as conn:
            session_json = conn.cursor().execute("SELECT session_json FROM sessions WHERE user_id = ?",
                                                 (user_id,)).fetchone()
            return Session.from_json(*session_json) if session_json else None

    def set_session(self, user_id: int, session: Session):
        with self._get_conn() as conn:
            conn.cursor().execute("INSERT OR REPLACE INTO sessions (user_id, session_json) VALUES(?, ?)", (user_id, session.to_json()))
            conn.commit()


# debug
# sq = SQliteSessionRepository()
# print(sq.get_session(100))
# sq.set_session(100, Session('gay', UserWord(None, 100, "orlov", "aboababba")))
# print(sq.get_session(100))
# sq.set_session(100, Session('gay', UserWord(None, 100, "orlov", "aboa")))
# print(sq.get_session(100))
# # print(*sq.get_all(), sep='\n')
