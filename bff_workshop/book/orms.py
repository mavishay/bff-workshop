import uuid

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import declarative_base

class BookORM(declarative_base()):
    __tablename__ = "books"

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())
