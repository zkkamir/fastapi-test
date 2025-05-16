from fastapi import status

from todo.main import app
from todo.models import Todos
from todo.routers.admin import get_db, get_current_user
from todo.tests.utils import (
    client,
    override_get_current_user,
    override_get_db,
    TestingSessionLocal,
)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    res = client.get("/admin/todo")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": test_todo.id,
            "title": test_todo.title,
            "description": test_todo.description,
            "priority": test_todo.priority,
            "complete": test_todo.complete,
            "owner_id": test_todo.owner_id,
        }
    ]


def test_admin_delete_todo(test_todo):
    res = client.delete(f"/admin/todo/{test_todo.id}")
    assert res.status_code == 204

    db = TestingSessionLocal()
    instance = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert instance is None


def test_admin_delete_todo_not_found(test_todo):
    res = client.delete("/admin/todo/999")
    assert res.status_code == 404
