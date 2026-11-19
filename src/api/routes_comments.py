from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import get_current_user
from src.api.schemas import CommentCreate, CommentOut
from src.services import request_service as svc
from src.repositories import comment_repo, request_repo

router = APIRouter(prefix="/requests", tags=["comments"])

def _can_view(user, req):
    if user["role"] in {"admin", "operator"}: return True
    if user["role"] == "executor" and req["executor_id"] == user["id"]: return True
    if user["role"] == "applicant" and req["applicant_id"] == user["id"]: return True
    return False

@router.get("/{request_id}/comments", response_model=list[CommentOut])
def list_comments(request_id: int, user=Depends(get_current_user)):
    req = request_repo.get_by_id(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if not _can_view(user, req):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return comment_repo.list_by_request(request_id)

@router.post("/{request_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(request_id: int, payload: CommentCreate, user=Depends(get_current_user)):
    return svc.add_comment(user, request_id, payload.text)
