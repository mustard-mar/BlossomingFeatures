import sqlite3

def create_table():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_item TEXT NOT NULL
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
#add_new_item("Test 2")
#print(get_all_items())
