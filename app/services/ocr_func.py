import sys
from pathlib import Path
from app.config import settings
from app.services.ocr.ocr_service import extract_text
from app.services.parser.vocabulary_parser import parse_vocabulary
import cv2



def img_to_word_list(image_bytes = bytes):
    ocr_result = extract_text(image_bytes)
    pairs = parse_vocabulary(ocr_result["text"])
    return pairs