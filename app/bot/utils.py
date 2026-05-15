import telebot
from typing import List, Optional


class TelegramGateway:
    def __init__(self, token: str):
        self._bot = telebot.TeleBot(token)

    def send_message(self, user_id: int, message: str, buttons: List[List[List[str]]] = []):
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            for row in buttons:
                tmp = [telebot.types.InlineKeyboardButton(text=text, callback_data=func) for text, func in row]
                keyboard.row(*tmp)
            message = self._bot.send_message(user_id, message, reply_markup=keyboard)
            return message.message_id
        except Exception as e:
            print(f"Telebot exception: {e}")
            return None

    def edit_message_text(self, user_id: int, message_id: int, text: str, buttons: List[List[List[str]]] = []) -> bool:
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                for row in buttons:
                    tmp = [telebot.types.InlineKeyboardButton(text=text, callback_data=func) for text, func in row]
                    keyboard.row(*tmp)
                self._bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=text,
                    reply_markup=keyboard
                )
                return True
            except telebot.apihelper.ApiException as e:
                if e.result.status_code == 400:
                    return False
                print(f"Telebot exception: {e}")
                return False
            except Exception as e:
                print(f"Telebot exception: {e}")
                return False

    def delete_button(self, user_id: int, message_id: int) -> bool:
        try:
            self._bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=None
            )
            return True
        except telebot.apihelper.ApiException as e:
            if e.result.status_code == 400:
                return False
            print(f"Telebot exception: {e}")
            return False
        except Exception as e:
            print(f"Telebot exception: {e}")
            return False
