import sqlite3


def add_database() -> None:
    with sqlite3.connect("sqlite3.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       hash_passwd TEXT,
                       is_admin BOOLEAN)""")

    connection.commit()
    connection.close()


def add_users(username: str, hash_passwd: str, is_admin: bool) -> None:
    with sqlite3.connect("sqlite3.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO users (username, hash_passwd, is_admin) VALUES (?, ?, ?)""",
            (username, hash_passwd, is_admin),
        )
    connection.commit()
    connection.close()


def get_users(username: str):
    with sqlite3.connect("sqlite3.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        return cursor.fetchone()


add_database()
