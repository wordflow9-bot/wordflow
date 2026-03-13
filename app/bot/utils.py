import telebot
from typing import List, Optional

bot = telebot.TeleBot('7875250913:AAGIkhrEcAOax3kwFDbb638JkEyOZuBHBsY')
# bot = telebot.TeleBot('8580430243:AAF9rhHRqakIT5FayWPQyx3Bh9OR8VB0C20')


def send_message(user_id: int, message: str, buttons: List[str] = []):
    keyboard = telebot.types.InlineKeyboardMarkup()
    tmp = [telebot.types.InlineKeyboardButton(text=text, callback_data=text) for text, func in buttons]
    keyboard.row(*tmp)
    bot.send_message(user_id, message,reply_markup=keyboard)
    
