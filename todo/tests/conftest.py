import pytest
from sqlalchemy import text

from todo.models import Todos, Users
from todo.routers.auth import bcrypt_context
from todo.tests.utils import engine, TestingSessionLocal


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


@pytest.fixture
def test_user():
    user = Users(
        username="test user",
        email="user@test.user",
        first_name="test",
        last_name="user",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="1111-111-1111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
