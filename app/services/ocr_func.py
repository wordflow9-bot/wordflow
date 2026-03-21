import sys
from pathlib import Path
from config import settings
from app.services.ocr.ocr_service import extract_text
from app.services.parser.vocabulary_parser import parse_vocabulary
import cv2
from typing import List
from app.core.models import Word


def img_to_word_list(image_bytes: bytes) -> List[Word]:
    ocr_result = extract_text(image_bytes)
    pairs = parse_vocabulary(ocr_result["text"])
    tmp = [Word(en=dict_['en'], ru=dict_['ru']) for dict_ in pairs]
    return tmp

