from deep_translator import GoogleTranslator
import re


class Translator:
    def __init__(self):
        self.en_in_ru = GoogleTranslator(source='en', target='ru')
        self.ru_in_en = GoogleTranslator(source='ru', target='en')

    @staticmethod
    def language(word: str) -> str:  # un - unknown
        is_ru = re.search('[а-яА-ЯёЁ]', word)
        is_en = re.search('[a-zA-Z]', word)
        if is_ru:
            return 'ru'
        if is_en:
            return 'en'
        return 'un'

    def translate(self, word: str) -> str:
        lang = Translator.language(word)
        if lang == 'ru':
            return self.ru_in_en.translate(word)
        if lang == 'en':
            return self.en_in_ru.translate(word)
        return "Язык нe понятен"
