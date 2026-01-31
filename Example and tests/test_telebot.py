import telebot
from telebot import types
import os
from dotenv import load_dotenv

import telebot_db

load_dotenv()
token = os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет!'
    )



@bot.message_handler(commands=['button'])
def send_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Добавить пункт"))
    keyboard.add(types.KeyboardButton("Узнать все пункты"))
    keyboard.add(types.KeyboardButton("Удалить пункт"))
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Добавить пункт","Узнать все пункты", "Удалить пункт"])
def handle_button(message):
    if message.text == "Добавить пункт":
        msg = bot.send_message(message.chat.id, "Введите название")
        bot.register_next_step_handler(msg, add_item)
    if message.text == "Удалить пункт":
        msg = bot.send_message(message.chat.id, "Введите номер пункта")
        bot.register_next_step_handler(msg, delete_item)
    if message.text == "Узнать все пункты":
        items = telebot_db.get_all_items()
        text_items = "\n".join([f"{id}: {text}" for id, text in items])
        bot.send_message(message.chat.id, text_items)

def add_item(message):
    item = message.text
    telebot_db.add_new_item(message.text)
    bot.send_message(message.chat.id, 'Добавлено!')
def delete_item(message):

    try:
        value = int(message.text)
        telebot_db.db_delete_item(value)
        bot.send_message(message.chat.id, 'Удалено!')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка!')

bot.infinity_polling()