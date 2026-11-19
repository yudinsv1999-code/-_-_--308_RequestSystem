from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import get_current_user
from src.api.schemas import RequestCreate, RequestAssign, StatusChange, RequestOut
from src.services import request_service as svc
from src.repositories import request_repo, comment_repo

router = APIRouter(prefix="/requests", tags=["requests"])

def _can_view(user, req):
    if user["role"] in {"admin", "operator"}:
        return True
    if user["role"] == "executor" and req["executor_id"] == user["id"]:
        return True
    if user["role"] == "applicant" and req["applicant_id"] == user["id"]:
        return True
    return False

@router.get("", response_model=list[RequestOut])
def list_requests(status_id: int | None = None,
                  category_id: int | None = None,
                  user=Depends(get_current_user)):
    filters = {}
    if status_id is not None: filters["status_id"] = status_id
    if category_id is not None: filters["category_id"] = category_id
    items = request_repo.list_all(filters)
    # «тихое сужение» по роли
    if user["role"] == "executor":
        items = [r for r in items if r["executor_id"] == user["id"]]
    elif user["role"] == "applicant":
        items = [r for r in items if r["applicant_id"] == user["id"]]
    return items

@router.get("/{request_id}", response_model=RequestOut)
def get_request(request_id: int, user=Depends(get_current_user)):
    req = request_repo.get_by_id(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if not _can_view(user, req):
        raise HTTPException(status_code=403, detail="Нет доступа к заявке")
    return req

@router.post("", response_model=RequestOut, status_code=201)
def create_request(payload: RequestCreate, user=Depends(get_current_user)):
    return svc.create_request(user, payload.title, payload.description, payload.category_id)

@router.post("/{request_id}/assign", response_model=RequestOut)
def assign_executor(request_id: int, payload: RequestAssign, user=Depends(get_current_user)):
    return svc.assign_executor(user, request_id, payload.executor_id)

@router.patch("/{request_id}/status", response_model=RequestOut)
def change_status(request_id: int, payload: StatusChange, user=Depends(get_current_user)):
    return svc.change_status(user, request_id, payload.status_id)
