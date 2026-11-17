import pytest
from src.database import connection
from src.services import request_service as svc
from src.services.exceptions import (
    ForbiddenError, InvalidTransitionError, ValidationError
)
from src.repositories import user_repo, status_repo, request_repo


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    db = tmp_path / "test.db"
    monkeypatch.setattr(connection, "DB_PATH", db)
    import sqlite3
    from pathlib import Path
    base = Path(__file__).parent.parent / "src" / "database"
    conn = sqlite3.connect(db)
    conn.executescript((base / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((base / "seed.sql").read_text(encoding="utf-8"))
    conn.commit(); conn.close()
    yield


def actor(email):
    return user_repo.get_by_email(email)


def test_create_request_by_applicant():
    a = actor("ivanov@example.com")
    r = svc.create_request(a, "Тест", "Описание", 1)
    assert r["number"].startswith("REQ-2026-")
    assert r["status_id"] == status_repo.get_by_name("Новая")["id"]


def test_applicant_cannot_assign_executor():
    a = actor("ivanov@example.com")
    with pytest.raises(ForbiddenError):
        svc.assign_executor(a, 1, 2)


def test_operator_assigns_executor():
    op = actor("sidorova@example.com")
    r = svc.assign_executor(op, 2, 2)   # заявка 2 без исполнителя
    assert r["executor_id"] == 2


def test_valid_status_transition():
    op = actor("sidorova@example.com")
    r = svc.change_status(op, 1, 3)   # В работе -> Выполнена
    assert r["status_id"] == 3


def test_invalid_status_transition():
    op = actor("sidorova@example.com")
    with pytest.raises(InvalidTransitionError):
        svc.change_status(op, 1, 4)   # В работе -> Закрыта (нельзя)


def test_executor_cannot_change_foreign_request():
    executor = actor("petrov@example.com")
    # заявка 2 без исполнителя -> executor не может
    with pytest.raises(ForbiddenError):
        svc.change_status(executor, 2, 2)


def test_executor_changes_own_request():
    executor = actor("petrov@example.com")
    r = svc.change_status(executor, 1, 3)   # заявка 1 назначена Петрову
    assert r["status_id"] == 3


def test_applicant_cannot_change_status():
    a = actor("ivanov@example.com")
    with pytest.raises(ForbiddenError):
        svc.change_status(a, 1, 3)


def test_empty_comment_rejected():
    op = actor("sidorova@example.com")
    with pytest.raises(ValidationError):
        svc.add_comment(op, 1, "") 



def test_reassign_same_executor_conflict():
    from src.services.exceptions import ConflictError
    op = actor("sidorova@example.com")
    svc.assign_executor(op, 2, 2)          # первое назначение
    with pytest.raises(ConflictError):
        svc.assign_executor(op, 2, 2)      # повторное — конфликт

def test_create_with_unknown_category():
    a = actor("ivanov@example.com")
    with pytest.raises(ValidationError):
        svc.create_request(a, "Тест", "Описание", 999)


def test_change_to_unknown_status():
    op = actor("sidorova@example.com")
    with pytest.raises(ValidationError):
        svc.change_status(op, 1, 999)
