import sqlite3


def insert_word(word):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
    connection.commit()
    connection.close()


def delete_word(word):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM words WHERE word = ?", (word,))
    connection.commit()
    connection.close()

    
def get_words_list():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT word FROM words")
    words_list = cursor.fetchall()
    connection.close()
    words_list = [word[0] for word in words_list]
    return words_list


def get_words_list_in_range(min_length, max_length):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT word FROM words WHERE LENGTH(word) BETWEEN ? AND ?", (min_length, max_length))
    words_list = cursor.fetchall()
    connection.close()
    words_list = [word[0] for word in words_list]
    print(words_list)
    return words_list
