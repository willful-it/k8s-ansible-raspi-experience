

import uuid

import pytest
from fastapi.testclient import TestClient
from main import app, get_db

from test_helper import (create_test_database, delete_database,
                         get_test_database_name)

client = TestClient(app)


@pytest.fixture
def test_main_db(scope="module"):
    app.dependency_overrides[get_db] = create_test_database
    yield app.dependency_overrides[get_db]()
    delete_database(get_test_database_name())


def _create_token(value: str = None):
    if not value:
        value = str(uuid.uuid4())

    data = {
        "value": value,
        "is_available": True
    }
    return client.post("/tokens", json=data)


def test_create_token(test_main_db):
    response = _create_token()

    assert response.status_code == 200


def test_get_tokens(test_main_db):
    _create_token("123")
    _create_token("456")
    _create_token("789")

    response = client.get("/tokens")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    tokens = [t for t in data if t["value"] in ('123', '456', '789')]
    assert len(tokens) == 3


def test_pop_token(test_main_db):
    _create_token("pop123")
    _create_token("pop456")
    _create_token("pop789")

    response = client.put("/tokens/pop")
    assert response.status_code == 200

    data = response.json()
    assert data["value"]
