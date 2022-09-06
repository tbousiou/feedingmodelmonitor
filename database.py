import sqlite3


def get_user_models():
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    results = cursor.execute("SELECT * FROM user_models").fetchall()

    cursor.close()
    connection.close()

    return results

