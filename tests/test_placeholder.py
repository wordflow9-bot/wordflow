# @WordFlow9_bot
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
from typing import Optional
import telebot
from config import settings
from app.repositories.sqlite_repositories import SQLiteWordRepository
from app.core.models import UserWord
from app.core.trainer_impl import Trainer


bot = telebot.TeleBot(settings.telegram_bot_token)
sq = SQLiteWordRepository()
# debug
sq.clear()
trainer = Trainer(sq)

def true(user_id, word_id):
    send_message(user_id, "You're right")


def false(user_id, word_id):
    send_message(user_id, "You're wrong")

def Start(user_id):
    id, word, translation = trainer.generate_question()
    buttons = ["true", "false"]
    training_message(user_id, id, "Is this true " + word + " == " + translation, buttons)
    
Function = dict() # TODO объявить функции и импортировать

def process(user_id: int, message: str):
    send_message(user_id, "OK", ["Start"]) # TODO: заменить на функцию из файла core


@bot.message_handler(commands=['start'])
def start(message):
    menu(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    word, translation = message.text.split()
    sq.add_word(message.from_user.id, word, translation)
    process(message.from_user.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_function(callback_obj):
    bot.edit_message_text(
        chat_id=callback_obj.message.chat.id,
        message_id=callback_obj.message.message_id,
        text=callback_obj.message.text,
        reply_markup=None  # ← это убирает ВСЕ inline-кнопки
    )
    # Function[callback_obj.data](callback_obj.from_user.id)
    data = callback_obj.data
    if (data == "Start") :
        Start(callback_obj.from_user.id)
    else:
        action, word_id_str = data.split(':', 1)
        word_id = int(word_id_str)
        if (action == "true"):
            action = True
        else:
            action = False
        correct, new_level = trainer.check_answer(word_id, action)
        if correct:
            bot.send_message(callback_obj.from_user.id, f"You're right! Correct: {correct}, New level: {new_level}%")
        else:
            bot.send_message(callback_obj.from_user.id, f"You're wrong. Correct: {not correct}, New level: {new_level}%")



def training_message(user_id: int, word_id: Optional[int], message: str, buttons = []):
    keyboard = telebot.types.InlineKeyboardMarkup()
    true_btn = telebot.types.InlineKeyboardButton("True", callback_data=f"true:{word_id}")
    false_btn = telebot.types.InlineKeyboardButton("False", callback_data=f"false:{word_id}")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(true_btn, false_btn)
    bot.send_message(user_id, message, reply_markup=keyboard)


def send_message(user_id: int, message: str, buttons = []):
    keyboard = telebot.types.InlineKeyboardMarkup()
    tmp = [telebot.types.InlineKeyboardButton(text=text, callback_data=text) for text in buttons]
    keyboard.row(*tmp)
    bot.send_message(user_id, message,reply_markup=keyboard)


TABLE = ["true", "false"]
def menu(user_id: int):
    send_message(user_id, "2 + 2 == 4?", TABLE)


bot.infinity_polling()

