from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.dependencies import get_db
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


@pytest.fixture()
def setup_account_book(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json=input_data(),
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    yield data


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_short_url(setup_account_book):
    response = client.post(
        "/short",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"url": f"{client.base_url}/v1/account-books/{setup_account_book['id']}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert 'short_url' in data

    response = client.get(data['short_url'])

    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == input_data()['amount']


def test_short_url_expire(setup_account_book):
    response = client.post(
        "/short",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"url": f"{client.base_url}/v1/account-books/{setup_account_book['id']}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert 'expire' in data
    expire = datetime.strptime(data['expire'], '%Y-%m-%dT%H:%M:%S')
    assert expire >= datetime.utcnow(), data


def input_data():
    return {
        "amount": 100,
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis.",
        "date": datetime.utcnow().date().strftime('%Y-%m-%d')
    }
