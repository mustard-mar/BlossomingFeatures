import telebot
from telebot import types
import os
from dotenv import load_dotenv

import telebot_db

load_dotenv()
token = os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(token)

#Заглушка для бд
counters={}
for i in range(1, 13):
    counters[f'item{i}']=[0,[]]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn_get_bingo = types.KeyboardButton('Получить бинго')
    btn_join_bingo = types.KeyboardButton('Принять участие в бинго')
    markup.add(btn_get_bingo)
    markup.add(btn_join_bingo)
    bot.send_message(message.chat.id, "Участвуйте в бинго!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Получить бинго","Принять участие в бинго"])
def handle_button(message):
    if message.text == "Получить бинго":
        welcome(message)
    if message.text == "Принять участие в бинго":
        print(f"Пользователь {message.from_user.id} принял участие в бинго")
#for admin
@bot.message_handler(commands=['button'])
def send_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Добавить пункт"))
    keyboard.add(types.KeyboardButton("Узнать все пункты"))
    keyboard.add(types.KeyboardButton("Удалить пункт"))
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)
#for admin
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
#for admin
def add_item(message):
    telebot_db.add_new_item(message.text)
    bot.send_message(message.chat.id, 'Добавлено!')
#for admin
def delete_item(message):

    try:
        value = int(message.text)
        telebot_db.db_delete_item(value)
        bot.send_message(message.chat.id, 'Удалено!')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка!')
#bingo_button
def create_keyboard():
    markup = types.InlineKeyboardMarkup()
    maxamount = 3
    text_complete = "✅"
    buttons = []
    for i in range(1, 13):
        key = f'item{i}'
        if counters[key][0]!=maxamount:
            text = f"{i} ({counters[key][0]}/{maxamount})"
        else:
            text = f"{i} {text_complete}"
        buttons.append(telebot.types.InlineKeyboardButton(text=text, callback_data=key))
    markup.add(*buttons, row_width=4)

    markup.row(telebot.types.InlineKeyboardButton(text="Обновить", callback_data="update"))

    return markup
#bingo
@bot.message_handler(commands=['btn_msg'])
def welcome(message):
    with open('bingo.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption='TestCaption',reply_markup=create_keyboard())
#bingo
@bot.callback_query_handler(func=lambda call: call.data[0:4] == 'item')
def callback_inline(call):
    item_id = call.data
    user_id = call.from_user.id

    if user_id not in counters[item_id][1]:
        counters[item_id][1].append(user_id)
        counters[item_id][0]+=1

    new_markup = create_keyboard()
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=new_markup
        )
    except telebot.apihelper.ApiTelegramException as e:
        # Если прилетело "сообщение не изменено", просто игнорим
        if "message is not modified" not in e.description:
            raise
    bot.answer_callback_query(call.id)
#bingo
@bot.callback_query_handler(func=lambda call: call.data == 'update')
def callback_inline_update(call):
    item_id = call.data
    user_id = call.from_user.id

    new_markup = create_keyboard()
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=new_markup
        )
    except telebot.apihelper.ApiTelegramException as e:
        # Если прилетело "сообщение не изменено", просто игнорим
        if "message is not modified" not in e.description:
            raise
    bot.answer_callback_query(call.id)

bot.infinity_polling()