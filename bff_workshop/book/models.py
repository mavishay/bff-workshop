import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: Optional[str] = Field(..., description="The id of the book.")
    title: str = Field(..., description="The title of the book.")
    author: str = Field(..., description="The author of the book.")

    updated_at: Optional[datetime.datetime] = Field(..., description="The date when this record was updated.")
    created_at: Optional[datetime.datetime] = Field(..., description="The date when this record was created.")

    class Config:
        orm_mode = True
        from_attributes = True


class BookInput(BaseModel):
    title: str
    author: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
