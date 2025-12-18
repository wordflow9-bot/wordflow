# @WordFlow9_bot

import telebot
from app.config import settings


bot = telebot.TeleBot(settings.telegram_bot_token)


Function = dict() # TODO объявить функции и импортировать

def true(user_id):
    send_message(user_id, "You're right")


def false(user_id):
    send_message(user_id, "You're wrong")


def prosess(user_id: int, message: str):
    send_message(user_id, "Your're " + message) # TODO: заменить на функцию из файла core


@bot.message_handler(commands=['start'])
def start(message):
    menu(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    prosess(message.from_user.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_function(callback_obj):
    bot.edit_message_text(
        chat_id=callback_obj.message.chat.id,
        message_id=callback_obj.message.message_id,
        text=callback_obj.message.text,
        reply_markup=None  # ← это убирает ВСЕ inline-кнопки
    )
    Function[callback_obj.data](callback_obj.from_user.id)



def send_message(user_id: int, message: str, buttons = []):
    keyboard = telebot.types.InlineKeyboardMarkup()
    tmp = [telebot.types.InlineKeyboardButton(text=text, callback_data=text) for text in buttons]
    keyboard.row(*tmp)
    bot.send_message(user_id, message,reply_markup=keyboard)


TABLE = ["true", "false"]
def menu(user_id: int):
    send_message(user_id, "2 + 2 == 4?", TABLE)


bot.infinity_polling()
