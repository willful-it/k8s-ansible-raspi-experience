from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True, index=True)
    is_available = Column(Boolean, default=True)
