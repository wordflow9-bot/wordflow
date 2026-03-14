from app.core.models import Session, SessionType
from app.repositories.sqlite_repositories import *
from app.bot.utils import send_message
from app.core.trainer_impl import Trainer
from deep_translator import GoogleTranslator

class Interaction:
    def __init__(self):
        self.user_word_repo = SQLiteWordRepository()
        self.session_repo = SQLiteSessionRepository()
        self.trainer = Trainer(self.user_word_repo)
        self.translator = GoogleTranslator(source='ru', target='en') # TODO: двустороний перевод

    def main_menu(self, user_id: int):
        self.session_repo.set_session(user_id, Session(SessionType.main_menu))
        buttons = [["Добавить слово", "Добавить слово"], ["Начать тренировку", "Начать тренировку"], ["Быстрый перевод", "Быстрый перевод"]]
        send_message(user_id, f"Что Вы хотите делать?", buttons)

    def add_word(self, user_id: int, message: str):
        words = list(message.split(' '))
        if len(words) != 2:
            # TODO : перевод от google
            send_message(user_id, "Введите ровно 2 слова")
            self.main_menu(user_id)
            return
        word, translation = words[0], words[1]
        self.user_word_repo.add_word(user_id, word, translation)
        send_message(user_id, f"Вы успешно добавили слово {word}, перевод для которого {translation}")
        self.main_menu(user_id)

    def check_translation(self, user_id: int, message: str):
        answer, level = self.trainer.check_answer(self.session_repo.get_session(user_id).crutch.id, message)
        if answer:
            answer = "верен"
        else:
            answer = "неверен"
        buttons = [["Eще раз", "Начать тренировку"], ["Главное меню", "Главное меню"]]
        send_message(user_id, f'Ваш ответ {answer}. Ваш успех в изучении слова {level}%', buttons)

    def process_translate(self, user_id: int, message: str):
        send_message(user_id, self.translator.translate(message))

    def process_message(self, user_id: int, message: str):
        session = self.session_repo.get_session(user_id)
        if session is None:
            send_message(user_id, "Привет")
            self.main_menu(user_id)
        elif session.session_type == SessionType.train_check_answer:  # TODO: тип сессии
            self.check_translation(user_id, message)
        elif session.session_type == SessionType.database_add_word:
            self.add_word(user_id, message)
        elif session.session_type == SessionType.translator_translate_word:
            self.process_translate(user_id, message)
        else:
            send_message(user_id, "Сначало выберите режим")
            self.main_menu(user_id)


    def button_ask_question(self, user_id: int):
        user_word = self.trainer.choose_word(user_id)
        if user_word is None:
            send_message(user_id, "Сначала добавьте слова")
            return
        send_message(user_id, f"Переведите слово {user_word.word}")
        self.session_repo.set_session(user_id,
            Session(SessionType.train_check_answer, user_word))

    def button_add_word(self, user_id: int):
        self.session_repo.set_session(user_id, Session(SessionType.database_add_word))
        send_message(user_id, f"Введите слово и перевод через пробел")

    def button_translate(self, user_id: int):
        self.session_repo.set_session(user_id, Session(SessionType.translator_translate_word))
        send_message(user_id, f"Введите слово на русском")

    def process_button(self, button: int):
        _dict = {"Добавить слово": self.button_add_word,
                 "Начать тренировку": self.button_ask_question,
                 "Главное меню": self.main_menu,
                 "Быстрый перевод": self.button_translate
                 }
        return _dict[button]
