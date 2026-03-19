import sqlite3
from typing import List, Optional
from app.core.models import UserWord, Session, Button, Word


# from app.config import settings


class SQLiteWordRepository:
    def __init__(self, db_path: str = '/wordflow/app/repositories/database.db'):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)  # TODO: что делает detect_types=sqlite3.PARSE_DECLTYPES)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    word_ru TEXT, 
                    word_en TEXT, 
                    total_cnt INTEGER, 
                    correct_cnt INTEGER)""")
            conn.commit()

    @staticmethod
    def _row_to_user_word(row: tuple) -> Optional[UserWord]:
        if row is None:
            return None
        db_id, user_id, word_ru, word_en, total_cnt, correct_cnt = row
        return UserWord(
            id=db_id,
            user_id=user_id,
            word=Word(ru=word_ru, en=word_en),
            total_cnt=total_cnt,
            correct_cnt=correct_cnt
        )

    def add_word(self, user_id: int, word: Word) -> UserWord:
        with self._get_conn() as conn:
            cur = conn.cursor().execute(
                "INSERT INTO words (user_id, word_ru, word_en, total_cnt, correct_cnt) VALUES (?, ?, ?, 0, 0)",
                (user_id, word.ru, word.en)
            )
            id_ = cur.lastrowid
            return self.get_by_id(id_)

    def get_all(self, user_id) -> List[UserWord]:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("SELECT * FROM words WHERE user_id = ?", (user_id,))
            rows = cur.fetchall()
            return [self._row_to_user_word(row) for row in rows]

    def get_by_id(self, word_id: int) -> Optional[UserWord]:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("SELECT * FROM words WHERE id = ?", (word_id,))
            row = cur.fetchone()
            return self._row_to_user_word(row)

    def delete_word(self, id_: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor().execute("DELETE FROM words WHERE id = ?", (id_,))
            conn.commit()
            # return cur.rowcount > 0
            return 1

    def adjust_mastery(self, id_: int, delta_correct_cnt: int = 1, delta_total_cnt: int = 1) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor().execute(
                "UPDATE words SET total_cnt = total_cnt + ?, correct_cnt = correct_cnt + ? WHERE id = ?",
                (delta_total_cnt, delta_correct_cnt, id_)
            )
            conn.commit()
            lvl = self.get_by_id(id_).mastery_level()
            return lvl

    def clear(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""DELETE FROM words""")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='words';")
            conn.commit()


class SQLiteSessionRepository:
    def __init__(self, db_path: str = '/wordflow/app/repositories/database.db'):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

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
            conn.cursor().execute("INSERT OR REPLACE INTO sessions (user_id, session_json) VALUES(?, ?)",
                                  (user_id, session.to_json()))
            conn.commit()


class SQLiteButtonRepository:
    def __init__(self, db_path: str = '/wordflow/app/repositories/database.db'):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS buttons(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message_id INTEGER,
                    metadata TEXT,
                    UNIQUE(user_id, message_id)
                )
            """)
            conn.commit()

    def get_button_metadata(self, user_id: int, message_id: int) -> Optional[Word]:
        with self._get_conn() as conn:
            row = conn.cursor().execute(
                "SELECT metadata FROM buttons WHERE user_id = ? AND message_id = ?",
                (user_id, message_id)
            ).fetchone()
            if row and row[0]:
                return Word.from_json(row[0])
            return None

    def add_button(self, user_id: int, button: Button):
        json_metadata = ''
        if button.metadata is not None:
            json_metadata = Word.to_json(button.metadata)
        with self._get_conn() as conn:
            conn.cursor().execute(
                "INSERT INTO buttons (user_id, message_id, metadata) VALUES(?, ?, ?)",
                (user_id, button.message_id, json_metadata)
            )
            conn.commit()

    def get_list_buttons(self, user_id: int) -> List[Button]:
        buttons = list()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message_id, metadata FROM buttons WHERE user_id = ?",
                (user_id,)
            )
            rows = cursor.fetchall()
            for row in rows:
                msg_id = row[0]
                meta_json = row[1]
                word_obj = None
                if meta_json:
                    word_obj = Word.from_json(meta_json)
                buttons.append(Button(message_id=msg_id, metadata=word_obj))
        return buttons

    def delete_button(self, user_id: int, message_id: int):
        with self._get_conn() as conn:
            conn.cursor().execute(
                "DELETE FROM buttons WHERE user_id = ? AND message_id = ?",
                (user_id, message_id)
            )
            conn.commit()
