import sqlite3

def create_table_items():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    # таблица для пунктов бинго
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_item TEXT NOT NULL
        )
        ''')
    #таблица для кнопок-пунктов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MenuBingo (
        button_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0
        )
        ''')
    #таблица для голосов(пользователей)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Votes (
        button_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (button_id,user_id),
        FOREIGN KEY (item_id) REFERENCES Items (item_id)
        )
        ''')
    connection.commit()
    connection.close()
def add_new_item(msg):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Items (name_item) VALUES (?)', (msg,))

    connection.commit()
    connection.close()
def get_all_items():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Items')
    items = cursor.fetchall()

    connection.close()

    return items
def db_delete_item(value):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Items WHERE id = ?', (value,))

    connection.commit()
    connection.close()


def create_table_calendar():
    connection = sqlite3.connect('calendar.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()
def add_new_event(title, date, description = ""):
    connection = sqlite3.connect('calendar.db')
    cursor = connection.cursor()
    if description=="":
        cursor.execute('INSERT INTO Events (title,date) VALUES (?,?)', (title,date))
    else:
        cursor.execute('INSERT INTO Events (title,date,description) VALUES (?,?,?)', (title, date,description))
    connection.commit()
    connection.close()
def get_all_events():
    connection = sqlite3.connect('calendar.db')
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Events')
    items = cursor.fetchall()

    connection.close()

    return items
def delete_db_calendar():
    connection = sqlite3.connect('calendar.db')
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM Events
        ''')
    connection.commit()
    connection.close()

#create_table_calendar()
#print(get_all_events())