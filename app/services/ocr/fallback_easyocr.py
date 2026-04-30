import cv2
import numpy as np
import easyocr
from .image_preprocessing import preprocess_image
import warnings


warnings.filterwarnings("ignore", message=".*pin_memory.*MPS.*")


reader = easyocr.Reader(['ru', 'en'], gpu=False)  # TODO: вернуть ocr


def extract_text_easyocr(input_image_bytes: bytes) -> str:
    np_arr = np.frombuffer(input_image_bytes, np.uint8)
    processed_input_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # processed_input_image = preprocess_image(input_image) #debug
    results = reader.readtext(processed_input_image)
    texts = [item[1] for item in results]
    return "\n".join(texts)