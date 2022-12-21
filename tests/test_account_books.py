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


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_account_books(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 100, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."},
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data


def test_update_account_books(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 100, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."},
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data

    response = client.put(
        f"/v1/account-books/{data['id']}",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 300}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == 300


def test_delete_account_books(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 100, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."},
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data

    response = client.delete(
        f"/v1/account-books/{data['id']}",
        headers={"Authorization": f"Bearer {setup_authorization}"}
    )

    assert response.status_code == 200


def test_list_account_books(setup_authorization):
    response = client.get(
        "/v1/account-books/",
        headers={"Authorization": f"Bearer {setup_authorization}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert type(data) == list


def test_get_account_books(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 100, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."},
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data

    response = client.get(
        f"/v1/account-books/{data['id']}",
        headers={"Authorization": f"Bearer {setup_authorization}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert 'date' in data


def test_copy_account_books(setup_authorization):
    response = client.post(
        "/v1/account-books",
        headers={"Authorization": f"Bearer {setup_authorization}"},
        json={"amount": 100, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lobortis."},
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data

    new_response = client.post(
        f"/v1/account-books/{data['id']}/copy",
        headers={"Authorization": f"Bearer {setup_authorization}"}
    )

    assert new_response.status_code == 201
    new_data = new_response.json()
    assert data['amount'] == new_data['amount']
