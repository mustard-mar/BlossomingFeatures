import sqlite3

def create_tables():
    connection = sqlite3.connect('../db/bingo.db')
    cursor = connection.cursor()
    # таблица для пунктов бинго
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_item TEXT NOT NULL
        )
        ''')
    #таблица для действий бинго
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_action TEXT NOT NULL
        )
        ''')
    #таблица для кнопок-пунктов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BingoButtons (
        button_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0,
        item_id INTEGER,
        action_id INTEGER,
        FOREIGN KEY (item_id) REFERENCES Items (id),
        FOREIGN KEY (action_id) REFERENCES Actions (id)
        )
        ''')
    #таблица для голосов(пользователей)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Votes (
        button_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (button_id, user_id)
        )
        ''')


    connection.commit()
    connection.close()
def add_new_item(msg):
    connection = sqlite3.connect('../my_database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Items (name_item) VALUES (?)', (msg,))

    connection.commit()
    connection.close()
def get_all_items():
    connection = sqlite3.connect('../my_database.db')
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Items')
    items = cursor.fetchall()

    connection.close()

    return items
def db_delete_item(value):
    connection = sqlite3.connect('../my_database.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Items WHERE id = ?', (value,))

    connection.commit()
    connection.close()

create_tables()