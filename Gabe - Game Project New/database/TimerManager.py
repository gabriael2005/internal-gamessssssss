import sqlite3

def update_timer_by_mode(time, mode):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE timer SET time=?WHERE mode=?", (time, mode))
    connection.commit()
    connection.close()

def get_time_by_mode(mode):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT time FROM timer where mode=?",(mode,))
    time = cursor.fetchone()[0]
    return time