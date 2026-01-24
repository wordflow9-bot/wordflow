# @WordFlow9_bot

import telebot
from typing import List, Optional
from app.core.interaction import Interaction
from app.bot.utils import send_message
# from app.config import settings


bot = telebot.TeleBot('7875250913:AAGIkhrEcAOax3kwFDbb638JkEyOZuBHBsY')
interaction = Interaction()


@bot.message_handler(commands=['help'])
def help(message):
    send_message(message.from_user.id, "Без коментариев.")

@bot.message_handler(commands=['start'])
def start(message):
    interaction.main_menu(message.from_user.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    interaction.process_message(message.from_user.id, message.text)

@bot.callback_query_handler(func=lambda call: True)
def callback_function(callback_obj):
    bot.edit_message_text(
        chat_id=callback_obj.message.chat.id,
        message_id=callback_obj.message.message_id,
        text=callback_obj.message.text,
        reply_markup=None  # ← это убирает ВСЕ inline-кнопки
    )
    interaction.process_button(callback_obj.data)(callback_obj.from_user.id)


bot.infinity_polling()
