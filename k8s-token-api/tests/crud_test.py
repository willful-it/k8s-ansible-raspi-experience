import os
import uuid
from pathlib import Path

import crud
import models
import pytest
from schemas import TokenCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def delete_database(name: str):
    for path in Path().rglob(name):
        os.remove(path)


@pytest.fixture
def test_db(scope="function"):
    name = f".{str(uuid.uuid4())}.sqlite"
    engine = create_engine(f"sqlite:///./{name}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    yield db
    delete_database(name)


def test_get_tokens(test_db):

    token = TokenCreate(value="xpto", is_available=True)
    crud.create_token(test_db, token)

    tokens = crud.get_tokens(test_db)

    assert tokens
