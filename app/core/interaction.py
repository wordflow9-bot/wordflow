from app.core.models import Session, SessionType
from app.repositories.sqlite_repositories import *
from app.bot.utils import TelegramGateway
from app.core.trainer_impl import Trainer
from app.core.translator import Translator


class Interaction:
    def __init__(self, bot_token: str):
        self.user_word_repo = SQLiteWordRepository()
        self.session_repo = SQLiteSessionRepository()
        self.button_repo = SQLiteButtonRepository()
        self.trainer = Trainer(self.user_word_repo)
        self.translator = Translator()
        self.gateway = TelegramGateway(bot_token)

    def send_message(self, user_id: int, message: str, buttons: Optional[List[List[str]]] = None,
                     metadata: Optional[Word] = None):
        if buttons is None:
            self.gateway.send_message(user_id, message)
        else:
            message_id = self.gateway.send_message(user_id, message, buttons)
            if message_id is not None:
                self.button_repo.add_button(user_id, Button(message_id=message_id, metadata=metadata))

    def delete_button(self, user_id: int, message_id: int):
        self.gateway.delete_button(user_id, message_id)
        self.button_repo.delete_button(user_id, message_id)

    def delete_buttons(self, user_id: int):
        for button in self.button_repo.get_list_buttons(user_id):
            self.delete_button(user_id, button.message_id)

    def main_menu(self, user_id: int, message_id: int = 0):
        self.session_repo.set_session(user_id, Session(SessionType.main_menu))
        self.delete_buttons(user_id)
        buttons = [["Тренировка", "Тренировка"],
                   ["Переводчик", "Переводчик"]]
        self.send_message(user_id, f"Что Вы хотите делать?", buttons)

    def add_word(self, user_id: int, message: str):
        self.user_word_repo.add_word(user_id, message, message)

    def list_words(self, user_id: int):
        user_words = self.user_word_repo.get_all(user_id)
        message = "Ваш список слов:\n"
        for user_word in user_words:
            message += f"{user_word.word.ru} {user_word.word.en} {user_word.mastery_level()}\n"
        self.send_message(user_id, message)

    def check_translation(self, user_id: int, message: str):
        answer, level = self.trainer.check_answer(self.session_repo.get_session(user_id).crutch.id, message)
        if answer:
            answer = "верен"
        else:
            answer = "неверен"
        buttons = [["Eще раз", "Тренировка"],
                   ["Меню", "Меню"]]
        self.send_message(user_id, f'Ваш ответ {answer}. Ваш успех в изучении слова {level}%', buttons)

    def process_translate(self, user_id: int, message: str):
        lang = self.translator.language(message)
        translation = self.translator.translate(message)
        if lang == 'ru':
            buttons = [["Добавить слово", "Переводчик, добавить слово"]]
            self.send_message(user_id, translation, buttons, metadata=Word(ru=message, en=translation))
        elif lang == 'en':
            buttons = [["Добавить слово", "Переводчик, добавить слово"]]
            self.send_message(user_id, translation, buttons, metadata=Word(en=message, ru=translation))
        elif lang == 'un':
            self.send_message(user_id, translation)

    def process_message(self, user_id: int, message: str):
        session = self.session_repo.get_session(user_id)
        if session is None:
            self.send_message(user_id, "Привет")
            self.main_menu(user_id)
        elif session.session_type == SessionType.train_check_answer:  # TODO: тип сессии
            self.check_translation(user_id, message)
        elif session.session_type == SessionType.database_add_word:
            self.add_word(user_id, message)
        elif session.session_type == SessionType.translator:
            self.process_translate(user_id, message)
        else:
            self.send_message(user_id, "Сначало выберите режим")
            self.main_menu(user_id)

    def button_start_training(self, user_id: int, message_id: int):
        self.delete_buttons(user_id)
        user_word = self.trainer.choose_word(user_id)
        if user_word is None:
            self.send_message(user_id, "Сначала добавьте слова")
            self.main_menu()
        else:
            self.send_message(user_id, f"Переведите слово {user_word.word.ru}")
            self.session_repo.set_session(user_id, Session(SessionType.train_check_answer, user_word))

    def button_translator(self, user_id: int, message_id: int):
        self.delete_buttons(user_id)
        self.session_repo.set_session(user_id, Session(SessionType.translator))
        self.send_message(user_id, f"Введите слово")

    def button_translator_add_word(self, user_id: int, message_id: int):
        word = self.button_repo.get_button_metadata(user_id, message_id)
        if word is not None:
            self.user_word_repo.add_word(user_id, word)
            self.delete_button(user_id, message_id)

    def button_add_word(self, user_id: int, message_id: int):
        return self.send_message(user_id, str(message_id))

    def process_button(self, button: str):
        _dict = {"Тренировка": self.button_start_training,
                 "Меню": self.main_menu,
                 "Добавить слово": self.button_add_word,
                 "Переводчик": self.button_translator,
                 "Переводчик, добавить слово": self.button_translator_add_word
                 }
        return _dict[button]
