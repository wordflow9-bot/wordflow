from google.cloud import vision
from .image_preprocessing import preprocess_image
from app.config import settings
import os


if settings.google_application_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials #debug, нужно передвинуть в (точку входа?)

try:
    client = vision.ImageAnnotatorClient()
except Exception:
    raise Exception


def extract_text_google(input_image_bytes: bytes) -> str:
    input_image = vision.Image(content=input_image_bytes)
    result = client.document_text_detection(image=input_image)
    if result.error.message:
        raise Exception(result.error.message)
    if not result.full_text_annotation:
        return ""
    return result.full_text_annotation.text