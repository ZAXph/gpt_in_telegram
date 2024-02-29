from telebot import TeleBot
import logging
from repository import *
from gpt import *
from transformers import AutoTokenizer

bot = TeleBot(token)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(func=check_commands)
def send_text_next(message):
    logging.info("Пользователь ввел неизвестную команду")
    bot.send_message(chat_id=message.chat.id, text="Данных команд не существует")


@bot.message_handler(func=check_next)
def send_text_next(message):
    logging.info("Пользователь продолжил тему разговора")
    data = open_json_file_and_write()
    bot.send_message(chat_id=message.chat.id, text="Ожидайте ответ")
    resp = gpt_processing_next(message.text, data["users"][message.chat.username])
    logging.info("Отправлен запрос GPT")
    if resp.status_code == 200 and 'choices' in resp.json():
        logging.info("Запрос прошел успешно")
        save_text(resp.json()['choices'][0]['message']['content'], message)
        bot.send_message(chat_id=message.chat.id, text=resp.json()['choices'][0]['message']['content'], reply_markup=markup)
        bot.send_message(chat_id=message.chat.id, text="Нажми: 'Продолжить' для продолжения объяснения.")
    else:
        logging.warning("Ошибка от GPT")
        bot.send_message(chat_id=message.chat.id, text=resp.json())


@bot.message_handler(content_types=["text"])
def send_text(message):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
    tokens = tokenizer.encode(message.text)
    if len(tokens) < MAX_TOKEN:
        start_json_file(message)
        logging.info("Пользователь добавлен в базу данных")
        bot.send_message(chat_id=message.chat.id, text="Ожидайте ответ", reply_markup=types.ReplyKeyboardRemove())
        resp = gpt_processing(message.text)
        logging.info("Отправлен запрос GPT")
        if resp.status_code == 200 and 'choices' in resp.json():
            logging.info("Запрос прошел успешно")
            save_text(resp.json()['choices'][0]['message']['content'], message)
            bot.send_message(chat_id=message.chat.id, text=resp.json()['choices'][0]['message']['content'], reply_markup=markup)
            bot.send_message(chat_id=message.chat.id, text="Нажми: 'Продолжить' для продолжения объяснения.")

        else:
            logging.warning("Ошибка от GPT")
            bot.send_message(chat_id=message.chat.id, text=resp.json())
    else:
        bot.send_message(chat_id=message.chat.id, text="Попробуйте задавать вопросы покороче")


@bot.message_handler(content_types=["video", "audio", "voice", "photo"])
def send_not_text(message):
    logging.warning("Пользователь не отправил текст")
    bot.send_message(chat_id=message.chat.id, text="Бот не работает ни с чем, кроме текста")


bot.polling()
