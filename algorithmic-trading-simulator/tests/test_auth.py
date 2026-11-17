from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.database import Base, get_db
from src.main import app
import src.models  # noqa: F401

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture(autouse=True)
def database() -> Generator[None, None, None]:
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_login_and_get_current_user() -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "email": "trader@example.com",
            "username": "trader",
            "password": "secure-password",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "trader@example.com"
    assert "password" not in body["user"]
    assert "password_hash" not in body["user"]
    assert body["token_type"] == "bearer"

    login = client.post(
        "/api/auth/login",
        json={"username": "trader", "password": "secure-password"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    current = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert current.status_code == 200
    assert current.json()["username"] == "trader"


def test_registration_rejects_duplicate_identity() -> None:
    payload = {
        "email": "trader@example.com",
        "username": "trader",
        "password": "secure-password",
    }
    assert client.post("/api/auth/register", json=payload).status_code == 201
    duplicate = client.post(
        "/api/auth/register",
        json={**payload, "email": "other@example.com"},
    )
    assert duplicate.status_code == 409


def test_invalid_credentials_and_missing_token_are_rejected() -> None:
    payload = {
        "email": "trader@example.com",
        "username": "trader",
        "password": "secure-password",
    }
    client.post("/api/auth/register", json=payload)
    bad_login = client.post(
        "/api/auth/login",
        json={"username": "trader", "password": "wrong-password"},
    )
    assert bad_login.status_code == 401
    assert client.get("/api/auth/me").status_code == 401
