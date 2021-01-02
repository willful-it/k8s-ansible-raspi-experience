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
               skip: int = 0, limit: int = 100) -> list:
    base_query = db.query(models.Token)

    if only_available:
        base_query = base_query.filter_by(is_available=True)

    return base_query.offset(skip).limit(limit).all()


def update_token(db: Session, token: schemas.TokenUpdate) -> models.Token:
    db_token = models.Token.query.get(token.id)

    db_token.is_available = token.is_available
    db_token.value = token.value

    db.commit()
    db.refresh(db_token)

    return db_token


def get_token_by_value(db: Session, value: str) -> models.Token:
    return db.query(models.Token).filter(models.Token.value == value).first()
