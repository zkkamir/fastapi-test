from fastapi import status

from todo.main import app
from todo.models import Todos
from todo.routers.todos import get_db, get_current_user
from todo.tests.utils import (
    client,
    override_get_current_user,
    override_get_db,
    TestingSessionLocal,
)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    res = client.get("/")
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


def test_read_one_authenticated(test_todo):
    res = client.get(f"/todo/{test_todo.id}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["title"] == test_todo.title


def test_read_one_authenticated_not_found():
    res = client.get("/todo/999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "Todo not found."}


def test_create_todo():
    data = {
        "title": "New Todo!",
        "description": "New todo description.",
        "priority": 2,
        "complete": True,
    }
    res = client.post("/todo", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    instance = db.query(Todos).filter(Todos.title == data["title"]).first()
    assert instance is not None


def test_update_todo(test_todo):
    data = {
        "title": "New Todo updated!",
        "description": "New todo description updated.",
        "priority": 1,
        "complete": False,
    }
    res = client.put("/todo/1", json=data)
    assert res.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    instance = db.query(Todos).filter(Todos.title == data["title"]).first()
    assert instance.description == data["description"]


def test_update_todo_not_found(test_todo):
    data = {
        "title": "New Todo updated!",
        "description": "New todo description updated.",
        "priority": 1,
        "complete": False,
    }
    res = client.put("/todo/999", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo(test_todo):
    res = client.delete(f"/todo/{test_todo.id}")
    assert res.status_code == 204
    db = TestingSessionLocal()
    instance = db.query(Todos).filter(Todos.title == test_todo.title).first()
    assert instance is None


def test_delete_todo_not_found(test_todo):
    res = client.delete("/todo/999")
    assert res.status_code == 404
