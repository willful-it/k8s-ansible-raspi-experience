import os
import uuid
from pathlib import Path

import crud
import models
from schemas import TokenCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


def delete_database(name: str):
    for path in Path().rglob(name):
        os.remove(path)


def create_random_database():
    name = f".{str(uuid.uuid4())}.sqlite"
    db = create_database(name)
    return db, name


def get_test_database_name():
    return ".test.sqlite"


def create_test_database():
    return create_database(get_test_database_name())


def create_database(name: str):
    engine = create_engine(
        f"sqlite:///./{name}",
        connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    return db


def create_tokens(test_db: Session, number_of_tokens: int = 10):
    for _ in range(number_of_tokens):
        token = TokenCreate(value=str(uuid.uuid4()), is_available=True)
        crud.create_token(test_db, token)
