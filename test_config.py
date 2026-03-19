# test_config.py
from app.config import settings
from google.cloud import vision
from pathlib import Path
import os


if settings.google_application_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

client = vision.ImageAnnotatorClient()

with open("tests/test.jpg", "rb") as f:
    content = f.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)

print(response.full_text_annotation.text)

# print("Токен бота:", settings.telegram_bot_token[:10] + "...")
# print("База данных:", settings.database_url)
