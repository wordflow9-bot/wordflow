# app/config.py
from pydantic_settings import BaseSettings
from pathlib import Path
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mindful-marking-474111-n5-9e4db07e6c18.json"

class Settings(BaseSettings):
    telegram_bot_token: str
    database_url: str = "sqlite:///./data/words.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Глобальный экземпляр — можно импортировать в других модулях
settings = Settings()