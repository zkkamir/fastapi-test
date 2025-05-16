from todo.main import app
from todo.routers.users import get_db, get_current_user
from todo.tests.utils import (
    client,
    override_get_current_user,
    override_get_db,
)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    res = client.get("/user")
    assert res.status_code == 200
    assert res.json()["username"] == test_user.username


def test_change_password_success(test_user):
    data = {"password": "testpassword", "new_password": "newpassword"}
    res = client.put("/user/change_password", json=data)
    assert res.status_code == 204


def test_change_password_invalid_current_password(test_user):
    data = {"password": "wrongpassword", "new_password": "newpassword"}
    res = client.put("/user/change_password", json=data)
    assert res.status_code == 401


def test_change_phone_number_success(test_user):
    res = client.put("/user/phone_number/2222222222")
    assert res.status_code == 204
