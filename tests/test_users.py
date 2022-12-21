import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.dependencies import get_db
from app.core.jwt_helper import validate_token
from app.db.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()


@pytest.fixture()
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_users(setup_db):
    input_data = {"email": "testing1@gmail.com", "password": "pwd123@@"}
    response = client.post(
        "/v1/users/register",
        json=input_data,
    )
    assert response.status_code == 201, response.text

    response = client.post(
        "/v1/users/login",
        json=input_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert validate_token(data["access_token"])

    response = client.post(
        "/v1/users/refresh",
        headers={"Authorization": f"Bearer {data['access_token']}"},
        json={"refresh_token": data['refresh_token']}
    )
    assert response.status_code == 200
    data = response.json()
    response = client.post(
        "/v1/users/logout",
        headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    assert response.status_code == 200
