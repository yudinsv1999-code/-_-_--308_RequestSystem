from src.database.connection import get_connection

def get_by_id(category_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Categories WHERE id = ?", (category_id,)).fetchone()
        return dict(row) if row else None

def list_all():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM Categories ORDER BY id")]
