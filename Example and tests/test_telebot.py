import telebot
from telebot import types
import os
from dotenv import load_dotenv

from db_scripts import bingo_db

load_dotenv()
token = os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(token)
#admin_id = int(os.getenv("ADMIN_ID"))

raw_ids = os.getenv("ADMIN_ID_LIST", "")
# Превращаем строку в список целых чисел
ids = [int(i) for i in raw_ids.split(",")] if raw_ids else []


#Заглушка для бд
maxamount = 2
counters={}
for i in range(1, 13):
    counters[f'item{i}']=[0,[]]

def setting_bingo_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Добавить пункт"))
    markup.add(types.KeyboardButton("Узнать все пункты"))
    markup.add(types.KeyboardButton("Удалить пункт"))
    markup.add(types.KeyboardButton("Сгенерировать новое бинго"))
    markup.add(types.KeyboardButton("Выйти изи настройки бинго"))
    return markup
def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Настроить бинго"))
    markup.add(types.KeyboardButton("Выйти из админки"))
    return markup
def user_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Получить бинго'))
    markup.add(types.KeyboardButton('Принять участие в бинго'))

    if user_id in ids:
        btn_admin_button = types.KeyboardButton('Войти в админку')
        markup.add(btn_admin_button)
    return markup
@bot.message_handler(commands=['start'])
def start(message):
    #print(f"Пользователь {message.from_user.id} пишет сообщения")
    bot.send_message(message.chat.id, "Участвуйте в бинго!", reply_markup=user_keyboard(message.from_user.id))


#for admin
@bot.message_handler(func=lambda message: True)
def handle_button(message):
    if message.text == "Получить бинго":
        welcome(message)
    if message.text == "Принять участие в бинго":
        print(f"Пользователь {message.from_user.id} принял участие в бинго")

    if message.from_user.id in ids:
        if message.text == "Войти в админку":
            bot.send_message(message.chat.id, "Да здравствует админка:", reply_markup=admin_keyboard())
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

        if message.text == "Настроить бинго":
            bot.send_message(message.chat.id, "Идём в настройку", reply_markup=setting_bingo_keyboard())
        if message.text == "Выйти изи настройки бинго":
            bot.send_message(message.chat.id, "Возвращаемся в админку", reply_markup=admin_keyboard())

        if message.text == "Выйти из админки":
            bot.send_message(message.chat.id, "Возврат к бинго", reply_markup=user_keyboard(message.from_user.id))

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
#bingo_btn
def inline_keyboard():
    markup = types.InlineKeyboardMarkup()
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
def welcome(message):
    with open('bingo.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption='TestCaption',reply_markup=inline_keyboard())

#bingo_func
@bot.callback_query_handler(func=lambda call: True)
def callback_inline_update(call):
    command = call.data
    if command == 'update':
        new_markup = inline_keyboard()
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
    if command[0:4]=='item':
        item_id = call.data
        user_id = call.from_user.id
        if (user_id not in counters[item_id][1]) and (counters[item_id][0] != maxamount):
            counters[item_id][1].append(user_id)
            counters[item_id][0] += 1

        new_markup = inline_keyboard()
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