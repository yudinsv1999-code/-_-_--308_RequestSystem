from src.repositories import request_repo, user_repo, status_repo
from src.services.exceptions import (
    NotFoundError, ForbiddenError, InvalidTransitionError, ValidationError
)

# Вариант 1: Новая->В работе->Выполнена->Закрыта
ALLOWED_TRANSITIONS = {
    1: {2},
    2: {3},
    3: {4},
    4: set(),
}

STATUS_CHANGERS = {"admin", "operator", "executor"}
CAN_ASSIGN = {"admin", "operator"}
CAN_CREATE = {"applicant", "operator", "admin"}


def create_request(actor, title, description, category_id):
    if actor["role"] not in CAN_CREATE:
        raise ForbiddenError("Роль не может создавать заявку")
    if not title or not description:
        raise ValidationError("title и description обязательны")
    new_status = status_repo.get_by_name("Новая")
    return request_repo.create(
        number=request_repo.next_number(),
        title=title, description=description,
        applicant_id=actor["id"], executor_id=None,
        status_id=new_status["id"], category_id=category_id,
    )


def assign_executor(actor, request_id, executor_id):
    if actor["role"] not in CAN_ASSIGN:
        raise ForbiddenError("Назначать исполнителя может admin/operator")
    req = _get_or_404(request_id)
    executor = user_repo.get_by_id(executor_id)
    if not executor or executor["role"] != "executor":
        raise ValidationError("Исполнитель не найден или не является executor")
    return request_repo.update(req["id"], executor_id=executor_id)


def change_status(actor, request_id, new_status_id):
    if actor["role"] not in STATUS_CHANGERS:
        raise ForbiddenError("Роль не может менять статус")
    req = _get_or_404(request_id)
    if actor["role"] == "executor" and req["executor_id"] != actor["id"]:
        raise ForbiddenError("Исполнитель может менять статус только своих заявок")
    if new_status_id not in ALLOWED_TRANSITIONS.get(req["status_id"], set()):
        raise InvalidTransitionError(
            f"Переход из статуса {req['status_id']} в {new_status_id} недопустим")
    return request_repo.update(req["id"], status_id=new_status_id)


def add_comment(actor, request_id, text):
    req = _get_or_404(request_id)
    if not text:
        raise ValidationError("Комментарий не может быть пустым")
    from src.repositories import comment_repo
    return comment_repo.create(req["id"], actor["id"], text)


def _get_or_404(request_id):
    req = request_repo.get_by_id(request_id)
    if not req:
        raise NotFoundError(f"Заявка {request_id} не найдена")
    return req
