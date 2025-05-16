from fastapi.testclient import TestClient

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from todo.database import Base
from todo.main import app


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


client = TestClient(app)
