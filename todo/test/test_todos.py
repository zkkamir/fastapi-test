from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker

from todo.database import Base
from todo.main import app
from todo.models import Todos
from todo.routers.todos import get_db, get_current_user


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "admin", "id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo", description="Test description", priority=5, owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()[0]["id"] == test_todo.id


def test_read_one_authenticated(test_todo):
    res = client.get("/todo/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == test_todo.id


def test_read_one_authenticated_not_found():
    res = client.get("/todo/999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "Todo not found."}


def test_create_todo():
    data = {
        'title': 'New Todo!',
        'description': 'New todo description.',
        'priority': 2,
        'complete': True
    }
    res = client.post('/todo', json=data)
    assert res.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    instance = db.query(Todos).filter(Todos.title == data['title']).first()
    assert instance is not None
