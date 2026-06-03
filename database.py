import sqlite3
import json

DB_NAME = "meetings.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        overview TEXT,
        summary_json TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_meeting(filename, result):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO meetings
    (filename, overview, summary_json)
    VALUES (?, ?, ?)
    """,
    (
        filename,
        result.get("overview", ""),
        json.dumps(result)
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")