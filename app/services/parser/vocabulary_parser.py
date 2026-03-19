import re
from .normalizer import normalize_text


CYRILLIC_PATTERN = re.compile(r"[а-яА-ЯёЁ]")
LATIN_PATTERN = re.compile(r"[a-zA-Z]")


def detect_language(text: str) -> str:
    if CYRILLIC_PATTERN.search(text):
        return "ru"
    if LATIN_PATTERN.search(text):
        return "en"
    return "unknown"


def clean(text: str) -> str:
    return re.sub(r"[^а-яА-ЯёËa-zA-Z\s]", "", text).strip()


def clean_en(text: str) -> str:
    return re.sub(r"[^a-zA-Z\s]", "", text).strip() #обработка смешанных строк добавить


def clean_ru(text: str) -> str:
    return re.sub(r"[^а-яА-ЯёЁ\s]", "", text).strip() #обработка смешанных строк добавить


def extract_elements(text: str):
    text = clean(text)
    elements = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ")
        for part in parts:
            part = part.strip()
            if part:
                elements.append(part)
    return elements


def split_mixed_elements(elements: list):
    if len(elements) < 2:
        return elements
    groups = []
    current_lang = detect_language(elements[0])
    current_group = [elements[0]]
    for word in elements[1:]:
        lang = detect_language(word)
        if lang == current_lang:
            current_group.append(word)
        else:
            groups.append(" ".join(current_group))
            current_group = [word]
            current_lang = lang
    groups.append(" ".join(current_group))
    return groups


def parse_vocabulary(text: str) -> list[dict]:
    normalized = normalize_text(text)
    elements = extract_elements(normalized)
    elements = split_mixed_elements(elements)
    pairs = []
    i = 0
    while i < len(elements) - 1:
        first = elements[i]
        second = elements[i + 1]
        lang1 = detect_language(first)
        lang2 = detect_language(second)
        if lang1 == "en" and lang2 == "ru":
            en = clean_en(first)
            ru = clean_ru(second)
            if en and ru:
                pairs.append({"en": en, "ru": ru})
            i += 2
            continue
        if lang1 == "ru" and lang2 == "en":
            en = clean_en(second)
            ru = clean_ru(first)
            if en and ru:
                pairs.append({"en": en, "ru": ru})
            i += 2
            continue
        i += 1
    return pairs