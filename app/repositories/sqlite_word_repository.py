import sqlite3

<<<<<<< Updated upstream
DB_LOCATION = "database.db"

def get_connection():
    """Создает новое соединение каждый раз"""
    return sqlite3.connect(DB_LOCATION)

def initialize():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER, word TEXT, translation TEXT, total_cnt INTEGER, correct_cnt INTEGER)""")
    con.commit()
    con.close()


def add_word(user_id: int, word: str, translation: str):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO words (user_id, word, translation, total_cnt, correct_cnt) VALUES (?, ?, ?, 0, 0)",
        (user_id, word, translation)
    )
    con.commit()
    con.close()


def get_random_word_data(user_id: int):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT id, word, translation FROM words WHERE user_id=? ORDER BY RANDOM() LIMIT 1",
        (user_id,)
    )
    result = cur.fetchone()
    con.close()
    return result


def query_performed(word_id: int, correct: bool):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE words SET total_cnt = total_cnt + 1 WHERE id=?",
        (word_id,)
    )
    if correct:
        cur.execute(
            "UPDATE words SET correct_cnt = correct_cnt + 1 WHERE id=?",
            (word_id,)
        )
    con.commit()
    con.close()
=======

# DB_LOCATION = "database.db"
# тут пока написана херня


class SQLiteWordRepository:
    def __init(self, db_path = "database.db"):
        con = sqlite3.connect(DB_LOCATION)
        cur = con.cursor()
        
    def initialize():
        cur.execute("""CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, word TEXT, translation TEXT, total_cnt INTEGER, correct_cnt INTEGER)""")
        con.commit()


    def add_word(user_id : int, word : str, translation : str):
        cur.execute("INSERT INTO words (user_id, word, translation, total_cnt, correct_cnt) VALUES ({}, '{}', '{}', 0, 0)"
                    .format(user_id, word, translation))
        con.commit()


    def get_random_word_data(user_id : int):
        cur.execute("SELECT (word_id, word, translation) FROM word WHERE user_id={} ORDER BY RANDOM() LIMIT 1".format(user_id))
        return cur.fetchone()


    def query_performed(word_id : int, correct : bool):
        cur.execute("UPDATE words SET total_cnt = total_cnt + 1 WHERE id={}".format(word_id))
        if correct:
            cur.execute("UPDATE words SET correct_cnt = correct_cnt + 1 WHERE id={}".format(word_id))
        con.commit()
>>>>>>> Stashed changes
