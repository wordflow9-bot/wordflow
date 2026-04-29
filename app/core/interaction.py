from app.core.models import Session, SessionType
from app.repositories.sqlite_repositories import *
from app.bot.utils import TelegramGateway
from app.core.trainer_impl import Trainer
from app.core.translator import Translator
from app.services.ocr_func import img_to_word_list
from typing import Callable


class Interaction:
    def __init__(self, bot_token: str):
        self.user_word_repo = SQLiteWordRepository()
        self.session_repo = SQLiteSessionRepository()
        self.button_repo = SQLiteButtonRepository()
        self.trainer = Trainer(self.user_word_repo)
        self.translator = Translator()
        self.gateway = TelegramGateway(bot_token)

    def _init_word(self, word: str):
        lang = self.translator.language(word)
        if lang == 'ru':
            return Word(ru=word, en=self.translator.translate(word))
        if lang == 'en':
            return Word(en=word, ru=self.translator.translate(word))
        return Word(ru=word, en=word)

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
        buttons = [["Добавить слово", "Добавить слово"],
                   ["Тренировка", "Тренировка"],
                   ["Переводчик", "Переводчик"]]
        self.send_message(user_id, f"Что Вы хотите делать?", buttons)

    def add_word(self, user_id: int, message: str):
        self.session_repo.set_session(user_id,
                                      Session(SessionType.database_add_word_choose_translation
                                              , self._init_word(message)))
        self.send_message(user_id, f'Выберите перевод или напишите свой',
                          buttons=[[self.translator.translate(message), "Выбрать перевод"]])

    def add_word_translation(self, user_id: int, message: str):
        user_word = self.session_repo.get_session(user_id).metadata
        lang = self.translator.language(message)
        if lang == 'ru':
            user_word.word.ru = message
        elif lang == 'en':
            user_word.word.en = message
        self.user_word_repo.add_word(user_id, user_word.word)
        self.main_menu(user_id)

    def list_words(self, user_id: int):
        user_words = self.user_word_repo.get_all(user_id)
        message = "Ваш список слов:\n"
        for user_word in user_words:
            message += f"{user_word.word.ru} {user_word.word.en} {user_word.mastery_level()}%\n"
        self.send_message(user_id, message)

    def ask_question(self, user_id: int):
        sess_type = self.session_repo.get_session(user_id).session_type
        if sess_type == SessionType.train_ru_check_answer:
            mode = "ru"
        elif sess_type == SessionType.train_en_check_answer:
            mode = "en"
        else:
            mode = "un"
        word = self.trainer.generate_question(user_id, mode)
        self.session_repo.set_session(user_id, Session(sess_type, metadata=word))
        if mode == "ru":
            self.send_message(user_id, message=f"Переведите слово \"{word.ru}\"")
        elif mode == "en":
            self.send_message(user_id, message=f"Переведите слово \"{word.en}\"")

    def check_translation(self, user_id: int, message: str):
        question = self.session_repo.get_session(user_id).metadata
        mode = self.session_repo.get_session(user_id).session_type
        if mode == SessionType.train_ru_check_answer:
            question.en = message
        elif mode == SessionType.train_en_check_answer:
            question.ru = message
        level = self.trainer.check_answer(user_id, word=question)
        buttons = [
            ["Eще раз", "Тренировка"],
            ["Меню", "Меню"]
        ]
        if level is None:
            answer = "неверен"
            self.send_message(user_id, f'Ваш ответ {answer}.', buttons)
        else:
            answer = "верен"
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
        elif session.session_type == SessionType.train_ru_check_answer or \
                session.session_type == SessionType.train_en_check_answer:  # TODO: тип сессии
            self.check_translation(user_id, message)
        elif session.session_type == SessionType.database_add_word:
            self.add_word(user_id, message)
        elif session.session_type == SessionType.database_add_word_choose_translation:
            self.add_word_translation(user_id, message)
        elif session.session_type == SessionType.translator:
            self.process_translate(user_id, message)
        else:
            self.send_message(user_id, "Сначала выберите режим")
            self.main_menu(user_id)

    def button_ask_question(self, user_id: int, message_id: int):
        self.delete_buttons(user_id)
        self.ask_question(user_id)

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
        self.delete_button(user_id, message_id)
        self.session_repo.set_session(user_id, Session(SessionType.database_add_word))
        self.send_message(user_id, f"Введите слово")

    def button_add_word_translation(self, user_id: int, message_id: int):
        self.delete_button(user_id, message_id)
        word = self.session_repo.get_session(user_id).metadata
        self.user_word_repo.add_word(user_id, word)
        self.main_menu(user_id)

    def button_tr_set_mode(self, user_id: int, message_id: int, mode: str):
        self.delete_button(user_id, message_id)
        if mode == 'ru':
            self.session_repo.set_session(user_id,
                                          Session(SessionType.train_ru_check_answer))
        elif mode == 'en':
            self.session_repo.set_session(user_id,
                                          Session(SessionType.train_en_check_answer))
        self.ask_question(user_id)

    def button_tr_choose_mode(self, user_id: int, message_id: int):
        self.delete_button(user_id, message_id)
        self.session_repo.set_session(user_id, Session(SessionType.train_choose_mode))
        buttons = [
            ["EN->RU", "Режим EN->RU"],
            ["RU->EN", "Режим RU->EN"]
        ]
        self.send_message(user_id, message="Выберите режим", buttons=buttons)

    def process_photo(self, user_id: int, photo_bytes: bytes):
        try:
            words = img_to_word_list(photo_bytes)
            if not words:
                self.send_message(user_id, "❌ Не удалось распознать текст")
                return
            for word in Word:
                self.send_message(user_id, f"{word.ru} – {word.en}",
                                  buttons=[["Добавить", "Переводчик, добавить слово"]], metadata=Word)
        except Exception as e:
            self.send_message(user_id, "❌ Не удалось распознать текст")
            print(f"Ошибка при распознании фото: {e}")
            self.main_menu(user_id)

    def process_button(self, button: str) -> Callable[[int, int], None]:
        _dict = {"Тренировка": self.button_tr_choose_mode,
                 "Меню": self.main_menu,
                 "Добавить слово": self.button_add_word,
                 "Выбрать перевод": self.button_add_word_translation,
                 "Переводчик": self.button_translator,
                 "Переводчик, добавить слово": self.button_translator_add_word,
                 "Режим RU->EN": lambda user_id, message_id: self.button_tr_set_mode(user_id, message_id, mode="ru"),
                 "Режим EN->RU": lambda user_id, message_id: self.button_tr_set_mode(user_id, message_id, mode="en")
                 }
        return _dict[button]



