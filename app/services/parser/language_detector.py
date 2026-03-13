import re


CYRILLIC_PATTERN = re.compile(r"[а-яА-ЯёЁ]")
LATIN_PATTERN = re.compile(r"[a-zA-Z]")


def detect_language(word: str) -> str:
    if CYRILLIC_PATTERN.search(word):
        return "ru"
    if LATIN_PATTERN.search(word):
        return "en"
    return "unknown"