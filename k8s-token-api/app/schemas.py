from pydantic import BaseModel


class TokenBase(BaseModel):
    value: str
    is_available: bool


class TokenCreate(TokenBase):
    pass


class Token(TokenBase):
    id: int

    class Config:
        orm_mode = True


class TokenUpdate(Token):
    pass
