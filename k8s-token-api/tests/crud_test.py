import os
import uuid
from pathlib import Path

import crud
import models
import pytest
from schemas import TokenCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


def _delete_database(name: str):
    for path in Path().rglob(name):
        os.remove(path)


def _create_tokens(test_db: Session, number_of_tokens: int = 10):
    for _ in range(number_of_tokens):
        token = TokenCreate(value=str(uuid.uuid4()), is_available=True)
        crud.create_token(test_db, token)


@pytest.fixture
def test_db(scope="function"):
    name = f".{str(uuid.uuid4())}.sqlite"
    engine = create_engine(f"sqlite:///./{name}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    yield db
    _delete_database(name)


def test_should_return_tokens_when_existing_in_the_db(test_db):
    number_of_tokens = 10
    _create_tokens(test_db, number_of_tokens)

    tokens = crud.get_tokens(test_db)

    assert len(tokens) == number_of_tokens


def test_should_update_token_fields(test_db):
    _create_tokens(test_db, 1)

    token = crud.get_tokens(test_db)[0]
    token.is_available = False

    updated_token = crud.update_token(test_db, token)
    db_token = crud.get_tokens(test_db)[0]

    assert not updated_token.is_available
    assert not db_token.is_available


def test_should_return_a_token_by_value(test_db):
    _create_tokens(test_db)

    token = crud.get_tokens(test_db)[0]
    token_by_value = crud.get_token_by_value(test_db, token.value)

    assert token.id == token_by_value.id
