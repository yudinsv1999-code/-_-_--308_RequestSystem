from fastapi import Header, HTTPException
from src.repositories import user_repo

def get_current_user(x_user_id: int | None = Header(default=None)):
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Требуется заголовок X-User-Id")
    user = user_repo.get_by_id(x_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
