import sqlite3


DB_LOCATION = ""


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
