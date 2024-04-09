from telebot import *

system_content = ("Ты — дружелюбный помощник во всем! А так же можешь поддерживать диалог! А так же ты поддерживаешь "
                  "только русский язык.")
assistant_content = "Давай разберем по шагам: "
token = ""


def check_next(message):
    return "продолжить" in message.text.lower()


def check_commands(message):
    return "/" in message.text.lower()


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(types.KeyboardButton("Продолжить"))


MAX_TOKEN = 512
