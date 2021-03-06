import random
from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def create_token(db: Session, token: schemas.TokenCreate) -> models.Token:
    db_token = models.Token(value=token.value, is_available=token.is_available)

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_tokens(db: Session, only_available: bool = False,
               skip: int = 0, limit: int = 100) -> List[models.Token]:
    base_query = db.query(models.Token)

    if only_available:
        base_query = base_query.filter_by(is_available=True)

    return base_query.offset(skip).limit(limit).all()


def update_token(db: Session, token: schemas.TokenUpdate) -> models.Token:
    db_token = db.query(models.Token).get(token.id)

    db_token.is_available = token.is_available
    db_token.value = token.value

    db.commit()
    db.refresh(db_token)

    return db_token


def get_token_by_value(db: Session, value: str) -> models.Token:
    return db.query(models.Token).filter(models.Token.value == value).first()


def pop_token(db: Session) -> models.Token:
    tokens = get_tokens(db, only_available=True)
    token_index = random.randint(0, len(tokens) - 1)
    token = tokens[token_index]

    token.is_available = False
    update_token(db, token)

    return token
