from src.database.connection import get_connection

def get_by_id(request_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM Requests WHERE id = ?", (request_id,)).fetchone()
        return dict(row) if row else None

def list_all(filters=None):
    filters = filters or {}
    sql = "SELECT * FROM Requests WHERE 1=1"
    params = []
    if "status_id" in filters:
        sql += " AND status_id = ?"; params.append(filters["status_id"])
    if "category_id" in filters:
        sql += " AND category_id = ?"; params.append(filters["category_id"])
    sql += " ORDER BY id"
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql, params)]

def next_number():
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM Requests").fetchone()
        return f"REQ-2026-{row['c'] + 1:04d}"

def create(number, title, description, applicant_id, executor_id, status_id, category_id):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO Requests
               (number, title, description, applicant_id, executor_id, status_id, category_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (number, title, description, applicant_id, executor_id, status_id, category_id),
        )
        conn.commit()
        return get_by_id(cur.lastrowid)

def update(request_id, **fields):
    allowed = {"title", "description", "executor_id", "status_id", "category_id"}
    keys = [k for k in fields if k in allowed]
    if not keys:
        return get_by_id(request_id)
    sets = ", ".join(f"{k} = ?" for k in keys)
    vals = [fields[k] for k in keys] + [request_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE Requests SET {sets} WHERE id = ?", vals)
        conn.commit()
        return get_by_id(request_id)
