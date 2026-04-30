# from .image_preprocessing import preprocess_image
from config import settings
from google.cloud import vision
import os


def _get_client():
    global _client
    if settings.google_application_credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
    try:
        _client = vision.ImageAnnotatorClient()
    except Exception:
        raise Exception
    return _client


def extract_text_google(input_image_bytes: bytes) -> str:
    client = _get_client()
    input_image = vision.Image(content=input_image_bytes)
    result = client.document_text_detection(image=input_image)
    if result.error.message:
        raise Exception(result.error.message)
    if not result.full_text_annotation:
        return ""
    return result.full_text_annotation.text
