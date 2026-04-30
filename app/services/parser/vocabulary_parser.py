import re
from typing import List

from .normalizer import normalize_text
from ...core.models import Word


def _is_mostly_cyrillic(text: str) -> bool:
    cyrillic_count = sum(1 for c in text if 'а' <= c.lower() <= 'я' or c in 'ёЁ')
    return cyrillic_count >= len(text) / 2


def _is_mostly_latin(text: str) -> bool:
    latin_count = sum(1 for c in text if 'a' <= c.lower() <= 'z')
    return latin_count >= len(text) / 2


CYRILLIC_REPLACEMENTS = {
    'O': 'О',
    'o': 'о',
    'P': 'Р',
    'p': 'р',
    'C': 'С',
    'c': 'с',
    'H': 'Н',
    'h': 'н',
    'B': 'В',
    'b': 'в',
    'X': 'Х',
    'x': 'х',
    'M': 'М',
    'm': 'м',
    'A': 'А',
    'a': 'а',
    'E': 'Е',
    'e': 'е',
    'Y': 'У',
    'y': 'у',
    'K': 'К',
    'k': 'к',
}
LATIN_REPLACEMENTS = {
    'О': 'O',
    'о': 'o',
    'Р': 'P',
    'р': 'p',
    'С': 'C',
    'с': 'c',
    'Н': 'H',
    'н': 'h',
    'В': 'B',
    'в': 'b',
    'Х': 'X',
    'х': 'x',
    'М': 'M',
    'м': 'm',
    'А': 'A',
    'а': 'a',
    'Е': 'E',
    'е': 'e',
    'У': 'Y',
    'у': 'y',
    'К': 'K',
    'к': 'k',
}


def _correct(text: str) -> str:
    if not text or len(text) <= 1:
        return text
    if _is_mostly_cyrillic(text):
        for lat, cyr in CYRILLIC_REPLACEMENTS.items():
            text = text.replace(lat, cyr)
        text =  re.sub(r"[^а-яА-ЯёЁ\s]", "", text).strip()
    elif _is_mostly_latin(text):
        for cyr, lat in LATIN_REPLACEMENTS.items():
            text = text.replace(cyr, lat)
        text = re.sub(r"[^a-zA-Z\s]", "", text).strip()
    return text


def _fix_case(text: str) -> str:
    if not text or len(text) <= 2:
        return text
    return text[0].upper() + text[1:].lower()


def detect_language(text: str) -> str:
    if _is_mostly_cyrillic(text):
        return "ru"
    if _is_mostly_latin(text):
        return "en"
    return "unknown"


def clean(text: str) -> str:
    return re.sub(r"[^а-яА-ЯёËa-zA-Z\s]", "", text).strip()


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


def split_mixed_elements(elements: List[str]):
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

    
def parse_vocabulary(text: str) -> List[Word]:
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
        if lang1 == "ru":
            lang1, lang2 = lang2, lang1
            first, second = second, first
        if lang1 == "en" and lang2 == "ru":
            en = _correct(first)
            en = _fix_case(en)
            ru = _correct(second)
            ru = _fix_case(ru)
            if en and ru:  # TODO: Нужна ли проверка
                pairs.append(Word(en=en, ru=ru))
            i += 2
            continue
        i += 1
    return pairs

