from src.database.connection import get_connection

def list_by_request(request_id):
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM Comments WHERE request_id = ? ORDER BY id", (request_id,))]

def create(request_id, user_id, text):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO Comments (request_id, user_id, text) VALUES (?, ?, ?)",
            (request_id, user_id, text),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM Comments WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
