from app.core.models import Session
from app.repositories.sqlite_repositories import *
from app.bot.utils import send_message
from app.core.trainer_impl import Trainer


class Interaction:
    def __init__(self, db_path='database.db'):
        self.user_word_repo = SQLiteWordRepository(db_path)
        self.session_repo = SQLiteSessionRepository(db_path)
        self.trainer = Trainer(self.user_word_repo)

    def main_menu(self, user_id: int):
        self.session_repo.set_session(user_id, Session("Main menu"))
        buttons = ["Добавить слово", "Начать тренировку"]
        send_message(user_id, f"Что ты хочешь делать?", buttons)

    def add_word(self, user_id: int, message: str):
        words = list(message.split(' '))
        if len(words) != 2:
            # TODO : перевод от google
            send_message(user_id, "Ты вообще умеешь считать количество слов, уебище?")
            return

        word, translation = words[0], words[1]
        self.user_word_repo.add_word(user_id, word, translation)
        self.main_menu(user_id)

    def check_translation(self, user_id: int, message: str):
        answer, level = self.trainer.check_answer(self.session_repo.get_session(user_id).crutch.id, message)
        if answer:
            answer = "верен"
        else:
            answer = "неверен"
        send_message(user_id, f'Ваш ответ {answer}. Ваш успех в изучение слова {level}%')
        self.main_menu(user_id)

    def process_message(self, user_id: int, message: str):
        session = self.session_repo.get_session(user_id)
        if session is None:
            send_message(user_id, "Привет")
            self.main_menu(user_id)
        elif session.session_type == "Waiting for answer": # TODO: тип сессии
            self.check_translation(user_id, message)
        elif session.session_type == "Waiting for word-translation":
            self.add_word(user_id, message)
        else:
            send_message(user_id, "Иди нахуй и прочитай описание бота")
            self.main_menu(user_id)

    def button_ask_question(self, user_id: int):
        user_word = self.trainer.choose_word(user_id)
        if user_word is None:
            send_message(user_id, "Сначала добавь слова пидр")
            return
        send_message(user_id, f"Переведите слово {user_word.word}")
        self.session_repo.set_session(user_id, Session("Waiting for answer", user_word))

    def button_add_word(self, user_id: int):
        self.session_repo.set_session(user_id, Session("Waiting for word-translation"))
        send_message(user_id, f"Введи слово и перевод через пробел")

    def process_button(self, button: str):
        _dict = {"Добавить слово": self.button_add_word,
                 "Начать тренировку": self.button_ask_question
                 }
        return _dict[button]
