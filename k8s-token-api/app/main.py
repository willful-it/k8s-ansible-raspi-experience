import random

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tokens", response_model=schemas.Token)
def create_token(token: schemas.TokenCreate, db: Session = Depends(get_db)):
    db_token = crud.get_token_by_value(db, value=token.value)

    if db_token:
        raise HTTPException(status_code=400, detail="Token already registered")

    return crud.create_token(db=db, token=token)


@app.get("/tokens", response_model=schemas.Token)
def get_tokens(db: Session = Depends(get_db)):
    return crud.get_tokens(db, only_available=True)


@app.put("/tokens/pop", response_model=schemas.Token)
def pop_token(db: Session = Depends(get_db)):

    tokens = crud.get_tokens(db, only_available=True)
    token_index = random.randint(0, len(tokens) - 1)
    token = tokens[token_index]

    token.is_available = False
    crud.update_token(db, token)

    return token
