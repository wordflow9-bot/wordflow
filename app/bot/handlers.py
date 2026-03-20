import telebot
from typing import List, Optional
from app.core.interaction import Interaction
# from app.config import settings

TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(TOKEN)
interaction = Interaction(TOKEN)


# @bot.message_handler(commands=['help']) TODO: написать help() в interaction
# def _help(message):
#     interaction.help(message.from_user.id)


@bot.message_handler(commands=['list'])
def _help(message):
    interaction.list_words(message.from_user.id)


@bot.message_handler(commands=['start'])
def start(message):
    interaction.main_menu(message.from_user.id)


@bot.message_handler(commands=['menu'])
def start(message):
    interaction.main_menu(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    interaction.process_message(message.from_user.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_function(callback_obj):
    interaction.process_button(callback_obj.data)(callback_obj.from_user.id, callback_obj.message.message_id)


bot.infinity_polling()

