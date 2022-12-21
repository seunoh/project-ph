import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.dependencies import get_db
from db.database import Base
from main import app

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


@pytest.fixture()
def setup_authorization(setup_db):
    response = client.post(
        "/v1/users/register",
        json={"email": "testing1@gmail.com", "password": "pwd123@@"},
    )
    assert response.status_code == 201
    response = client.post(
        "/v1/users/login",
        json={"email": "testing1@gmail.com", "password": "pwd123@@"},
    )
    data = response.json()
    access_token = data["access_token"]
    yield access_token
    response = client.post(
        "/v1/users/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_short_url(setup_authorization):
    input_data = {"amount": 100,
                  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."}
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json=input_data,
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data

    response = client.post(
        "/short",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"url": f"{client.base_url}/v1/account-books/{data['id']}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert 'short_url' in data

    response = client.get(data['short_url'])

    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == input_data['amount']
