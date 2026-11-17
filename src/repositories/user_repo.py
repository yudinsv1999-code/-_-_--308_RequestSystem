from src.database.connection import get_connection

def get_by_id(user_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

def get_by_email(email):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

def list_all():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM Users ORDER BY id")]
