import telebot
from typing import List, Optional
from app.core.interaction import Interaction
from config import settings
from io import BytesIO


TOKEN = settings.telegram_bot_token
bot = telebot.TeleBot(TOKEN)
interaction = Interaction(TOKEN)


# @bot.message_handler(commands=['help']) TODO: написать help() в interaction
# def _help(message):
#     interaction.help(message.from_user.id)


@bot.message_handler(commands=['list'])
def _list(message):
    interaction.list_words(message.from_user.id)


@bot.message_handler(commands=['help'])
def _help(message):
    interaction.command_help(message.from_user.id)


@bot.message_handler(commands=['start'])
def start(message):
    interaction.main_menu(message.from_user.id)


@bot.message_handler(commands=['train'])
def train(message):
    interaction.command_tr_choose_mode(message.from_user.id)


@bot.message_handler(commands=['add'])
def train(message):
    interaction.command_add_word(message.from_user.id)


@bot.message_handler(commands=['menu'])
def menu(message):
    interaction.main_menu(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    interaction.process_message(message.from_user.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_function(callback_obj):
    interaction.process_button(callback_obj.data)(callback_obj.from_user.id, callback_obj.message.message_id)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        interaction.process_photo(user_id, downloaded_file)
    except Exception as e:
        print(f"Ошибка при приеме фото : {e}")


@bot.message_handler(commands=['clear'])
def clear_all_words(message):
    interaction.clear_all_words(message.from_user.id)
