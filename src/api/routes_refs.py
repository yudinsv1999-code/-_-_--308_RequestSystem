from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import get_current_user
from src.api.schemas import UserOut
from src.repositories import category_repo, status_repo, user_repo

router = APIRouter(tags=["refs"])

@router.get("/categories")
def list_categories(user=Depends(get_current_user)):
    return category_repo.list_all()

@router.get("/statuses")
def list_statuses(user=Depends(get_current_user)):
    return status_repo.list_all()

@router.get("/users", response_model=list[UserOut])
def list_users(user=Depends(get_current_user)):
    if user["role"] not in {"admin", "operator"}:
        raise HTTPException(status_code=403, detail="Только admin/operator")
    return user_repo.list_all()

@router.get("/users/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
