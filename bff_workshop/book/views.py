from typing import List, Any, Dict

from fastapi import APIRouter
from fastapi_sqlalchemy import db

from bff_workshop.book.models import Book, BookInput, BookUpdate
from bff_workshop.book.orms import BookORM

router = APIRouter()


@router.get("")
def get_books_list() -> List[Book]:
    return db.session.query(BookORM).all()


@router.post("")
def create_book(book: BookInput) -> Book:
    book_orm = BookORM(**book.__dict__)
    db.session.add(book_orm)
    db.session.commit()
    db.session.refresh(book_orm)
    return Book.from_orm(book_orm)


@router.get("/{book_id}")
def get_book(book_id: str) -> Book:
    return Book.from_orm(db.session.query(BookORM).get(book_id))


@router.put("/{book_id}")
def update_book(book_id: str, book: BookUpdate) -> Book:
    book_orm = db.session.query(BookORM).get(book_id)
    for field, value in book.__dict__.items():
        if value is not None:
            setattr(book_orm, field, value)
    db.session.commit()

    return Book.from_orm(book_orm)


@router.delete("/{book_id}")
def delete_book(book_id: str) -> Dict[str, Any]:
    db.session.query(BookORM).filter(BookORM.id == book_id).delete()
    db.session.commit()
    return {"status": "success", "message": f"{book_id} deleted successfully!"}
