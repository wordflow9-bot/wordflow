# test_config.py
from app.config import settings
from google.cloud import vision
from pathlib import Path
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mindful-marking-474111-n5-9e4db07e6c18.json"

client = vision.ImageAnnotatorClient()

with open("tests/test.jpg", "rb") as f:
    content = f.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)

print(response.full_text_annotation.text)

# print("Токен бота:", settings.telegram_bot_token[:10] + "...")
# print("База данных:", settings.database_url)
