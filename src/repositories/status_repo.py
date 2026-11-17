from src.database.connection import get_connection

def get_by_id(status_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Statuses WHERE id = ?", (status_id,)).fetchone()
        return dict(row) if row else None

def get_by_name(name):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Statuses WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None

def list_all():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM Statuses ORDER BY id")]
