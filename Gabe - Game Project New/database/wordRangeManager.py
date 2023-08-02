import sqlite3

def insert_word_range(min_value, max_value):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ranges (min, max) VALUES (?, ?)", (min_value, max_value))
    connection.commit()
    connection.close()

def delete_word_range_by_id(word_range_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ranges WHERE id = ?", (word_range_id,))
    connection.commit()
    connection.close()

def get_word_ranges_list():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ranges")
    word_ranges_list = cursor.fetchall()
    connection.close()
    return word_ranges_list    