# test_config.py
from app.config import settings

print("Токен бота:", settings.telegram_bot_token[:10] + "...")
print("База данных:", settings.database_url)
