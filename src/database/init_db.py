import sqlite3
from pathlib import Path

BASE = Path(__file__).parent
DB = BASE / "app.db"

def init_db():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((BASE / "seed.sql").read_text(encoding="utf-8"))
    conn.commit()
    return conn

if __name__ == "__main__":
    conn = init_db()
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    requests = conn.execute(
        "SELECT id, number, title, status_id FROM Requests").fetchall()
    categories = conn.execute("SELECT COUNT(*) FROM Categories").fetchone()[0]
    print("TABLES:", tables)
    print("REQUESTS:", requests)
    print("CATEGORIES:", categories)
    conn.close()
