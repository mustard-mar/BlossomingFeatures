import telebot
from telebot import types
import os
from dotenv import load_dotenv

import telebot_db

load_dotenv()
token = os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(token)

counters = {f'item{i}': 0 for i in range(1, 13)}
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
        text_items = "\n".join([f"{i}: {text}" for i, text in items])
        bot.send_message(message.chat.id, text_items)

def add_item(message):
    telebot_db.add_new_item(message.text)
    bot.send_message(message.chat.id, 'Добавлено!')

def delete_item(message):

    try:
        value = int(message.text)
        telebot_db.db_delete_item(value)
        bot.send_message(message.chat.id, 'Удалено!')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка!')

def create_keyboard():
    markup = types.InlineKeyboardMarkup()

    button_1 = telebot.types.InlineKeyboardButton(text=f"1 ({counters['item1']}/{15})", callback_data='item1')
    button_2 = telebot.types.InlineKeyboardButton(text=f"2 ({counters['item2']}/{15})", callback_data='item2')
    button_3 = telebot.types.InlineKeyboardButton(text=f"3 ({counters['item3']}/{15})", callback_data='item3')
    button_4 = telebot.types.InlineKeyboardButton(text=f"4 ({counters['item4']}/{15})", callback_data='item4')
    button_5 = telebot.types.InlineKeyboardButton(text=f"5 ({counters['item5']}/{15})", callback_data='item5')
    button_6 = telebot.types.InlineKeyboardButton(text=f"6 ({counters['item6']}/{15})", callback_data='item6')
    button_7 = telebot.types.InlineKeyboardButton(text=f"7 ({counters['item7']}/{15})", callback_data='item7')
    button_8 = telebot.types.InlineKeyboardButton(text=f"8 ({counters['item8']}/{15})", callback_data='item8')
    button_9 = telebot.types.InlineKeyboardButton(text=f"9 ({counters['item9']}/{15})", callback_data='item9')
    button_10 = telebot.types.InlineKeyboardButton(text=f"10 ({counters['item10']}/{15})", callback_data='item10')
    button_11 = telebot.types.InlineKeyboardButton(text=f"11 ({counters['item11']}/{15})", callback_data='item11')
    button_12 = telebot.types.InlineKeyboardButton(text=f"12 ({counters['item12']}/{15})", callback_data='item12')
    markup.row(button_1, button_2, button_3, button_4)
    markup.row(button_5, button_6, button_7, button_8)
    markup.row(button_9, button_10, button_11, button_12)
    return markup

@bot.message_handler(commands=['btn_choice'])
def send_keyboard(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    itembtn5 = types.KeyboardButton('5')
    itembtn6 = types.KeyboardButton('6')
    itembtn7 = types.KeyboardButton('7')
    itembtn8 = types.KeyboardButton('8')
    itembtn9 = types.KeyboardButton('9')
    itembtn10 = types.KeyboardButton('10')
    itembtn11 = types.KeyboardButton('11')
    itembtn12 = types.KeyboardButton('12')
    markup.row(itembtn1, itembtn2,itembtn3,itembtn4)
    markup.row(itembtn5, itembtn6,itembtn7,itembtn8)
    markup.row(itembtn9, itembtn10,itembtn11,itembtn12)
    bot.send_message(message.chat.id, "Choose one number:", reply_markup=markup)

@bot.message_handler(commands=['btn_msg'])
def welcome(message):
    with open('bingo.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption='TestCaption',reply_markup=create_keyboard())

@bot.callback_query_handler(func=lambda call: call.data[0:4] == 'item')
def callback_inline(call):
    item_id = call.data
    counters[item_id] = counters.get(item_id, 0) + 1

    new_markup = create_keyboard()

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=new_markup
    )
    #bot.send_message(call.message.chat.id, 'Выбран '+ call.data[4:])
    bot.answer_callback_query(call.id)

bot.infinity_polling()