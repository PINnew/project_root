import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("humans.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_photo(filename):
    conn = sqlite3.connect("humans.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photos (filename, created_at) VALUES (?, ?)", (filename, datetime.now()))
    conn.commit()
    conn.close()


def get_photos_by_date(start_date, end_date):
    conn = sqlite3.connect("humans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM photos WHERE created_at BETWEEN ? AND ?", (start_date, end_date))
    photos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return photos
