import requests
import json
import random
import os
from dotenv import load_dotenv


def read_meta(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return(json_data)
    else:
        return(f"Ошибка: {response.status_code}")
def read_info(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return (json_data)
    else:
        return (f"Ошибка: {response.status_code}")
def send_mess(bot_token,chat_id,message_text):
    # https://api.telegram.org/bot{ТОКЕН}/sendMessage? chat_id={ID-ЧАТА}& text={СООБЩЕНИЕ}
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Параметры запроса
    params = {
        "chat_id": chat_id,
        "text": message_text
    }

    response = requests.get(url, params=params)

    # Обработка ответа сервера
    if response.status_code == 200:
        json_data = response.json()
        return(json_data)
    else:
        return(f"Error: {response.status_code}")
def send_list(bot_token,chat_id,rand_list):
    message_text = "\n".join(rand_list)
    send_mess(bot_token,chat_id,message_text)
def generate_list(source_file, fav_file, number):
    #Генерирует json file с списком строчек(сообщений)
    # брем строчки из общего файла, делаем список, берем n строчек и запихиваем их в другой json file

    tmp_dict = json_to_dict(source_file)
    # Выбираем 6 случайных ключей
    random_keys = random.sample(list(tmp_dict.keys()), number)

    # Собираем новый словарь из этих ключей
    new_dict = {key: tmp_dict[key] for key in random_keys}
    dict_to_json(new_dict,fav_file)
def json_to_dict(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
def dict_to_json(new_dict,file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(new_dict, f, ensure_ascii=False, indent=4)
def json_to_list(file):
    return list(json_to_dict(file).values())

load_dotenv()
token = os.getenv("BOT_TOKEN")
chat = os.getenv("CHAT_ID")
#generate_list('el_list.json','fav_list.json',5)

send_list(token,chat,json_to_list('fav_list.json'))