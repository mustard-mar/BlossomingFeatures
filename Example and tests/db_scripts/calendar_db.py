import sqlite3
def create_table_calendar():
    connection = sqlite3.connect('../db/calendar.db')
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
    connection = sqlite3.connect('../calendar.db')
    cursor = connection.cursor()
    if description=="":
        cursor.execute('INSERT INTO Events (title,date) VALUES (?,?)', (title,date))
    else:
        cursor.execute('INSERT INTO Events (title,date,description) VALUES (?,?,?)', (title, date,description))
    connection.commit()
    connection.close()
def get_all_events():
    connection = sqlite3.connect('../calendar.db')
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Events')
    items = cursor.fetchall()

    connection.close()

    return items
def delete_db_calendar():
    connection = sqlite3.connect('../calendar.db')
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM Events
        ''')
    connection.commit()
    connection.close()
create_table_calendar()