import re
from .normalizer import normalize_text


CYRILLIC_PATTERN = re.compile(r"[а-яА-ЯёЁ]")
LATIN_PATTERN = re.compile(r"[a-zA-Z]")


def detect_language(word: str) -> str:
        if CYRILLIC_PATTERN.search(word):
            return "ru"
        if LATIN_PATTERN.search(word):
            return "en"
        return "unknown"


def clean_en(word: str) -> str:
    return re.sub(r"[^a-zA-Z\-]", "", word).strip()

def clean_ru(word: str) -> str:
    return re.sub(r"[^а-яА-ЯёЁ\s\-]", "", word).strip()

    
def parse_vocabulary(text: str) -> list[dict]:
    normalized_output = normalize_text(text)
    pairs = []
    for line in normalized_output.split("\n"):
        if "-" not in line:
            continue
        parts = line.split("-", 1)
        if len(parts) != 2:
            continue
        left = parts[0].strip()
        right = parts[1].strip()
        lang_left = detect_language(left)
        lang_right = detect_language(right)
        en_word = None
        ru_word = None
        if lang_left == "en" and lang_right == "ru":
            left = clean_en(left)
            en_word = left
            right = clean_ru(right)
            ru_word = right
        elif lang_left == "ru" and lang_right == "en":
            right = clean_en(right)
            en_word = right
            left = clean_ru(left)
            ru_word = left
        if en_word and ru_word:
            pairs.append({
                "en": en_word,
                "ru": ru_word
            })
    return pairs