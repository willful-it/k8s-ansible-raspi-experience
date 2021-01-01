import uuid

import pytest

from persistence import PersistenceService


@pytest.fixture
def test_db(scope="function"):
    db = PersistenceService(filename=f".{str(uuid.uuid4())}.sqlite")
    yield db
    db.delete_database()


def test_count_token_return_zero(test_db):
    assert test_db.count_tokens() == 0


def test_count_token_return_one(test_db):
    test_db.create_token("sometoken")
    assert test_db.count_tokens() == 1


def test_use_two_persistence_services():
    name = f".{str(uuid.uuid4())}.sqlite"
    ps1 = PersistenceService(filename=name)
    ps2 = PersistenceService(filename=name)

    ps1.delete_database()
    ps2.delete_database()


def test_use_token(test_db):
    token = test_db.create_token("sometoken")
    test_db.use_token(token.id)

    assert test_db.count_tokens() == 0


def test_get_tokens(test_db):
    test_db.create_token("sometoken")
    test_db.create_token("sometoken2")
    test_db.create_token("sometoken3")

    tokens = test_db.get_available_tokens()

    assert len(tokens) == 3
