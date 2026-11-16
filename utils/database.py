
import sqlite3
from datetime import datetime

DB_NAME = "promptlab.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            category TEXT,
            prompt_type TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_prompt(title, prompt, category, prompt_type):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prompts
        (title, prompt, category, prompt_type, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        prompt,
        category,
        prompt_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_all_prompts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM prompts
        ORDER BY id DESC
    """)

    prompts = cursor.fetchall()
    connection.close()

    return prompts


def search_prompts(keyword):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM prompts
        WHERE title LIKE ? OR prompt LIKE ? OR category LIKE ?
        ORDER BY id DESC
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    prompts = cursor.fetchall()
    connection.close()

    return prompts


def delete_prompt(prompt_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM prompts WHERE id = ?",
        (prompt_id,)
    )

    connection.commit()
    connection.close()
