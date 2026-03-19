import sys
from pathlib import Path
from app.config import settings
from app.services.ocr.ocr_service import extract_text
from app.services.parser.vocabulary_parser import parse_vocabulary
import cv2
# import os


# if settings.google_application_credentials:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials


IMAGE_PATH = Path("tests/test.jpg")


def main():
    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    ocr_result = extract_text(image_bytes)
    print("\nOCR ENGINE:", ocr_result["engine"])
    print("\nRAW OCR TEXT:\n")
    print(ocr_result["text"])
    pairs = parse_vocabulary(ocr_result["text"])
    print("\nPARSED WORDS:\n")
    for pair in pairs:
        print(f"{pair["en"]} -> {pair["ru"]}\n")
    print(f"TOTAL WORDS: {len(pairs)}")
if __name__ == "__main__":
    main()