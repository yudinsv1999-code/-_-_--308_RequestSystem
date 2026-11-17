import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "app.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # доступ к колонкам по имени
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
