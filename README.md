# Welcome for Tikal Python BFF workshop

## Prerequisites

Before we began please make sure you have `python` and `poetry` installed on your computer. 

Run `python --version` or `python3 --version` and look for something like that 
> Python 3.12.3 

if it's not installed run `brew install python` and try the following step again.

---

In this workshop we will use `poetry` as package management tool please verify it is installed by running `poetry --version` the output should look like something like that 
> Poetry (version 1.8.3)

if it's not installed install it running `curl -sSL https://install.python-poetry.org | python3 -`

## First step - Creating our project

In order to create a new python project got the directory you want to create your project in using the CLI and
run `poetry new bff_workshop`
This will create new folder with several files. **Try it now!**. 

If everything worked as planned it should have return you this message 
> Created package bff_workshop in bff_workshop

Let's open the new created folder with a code editor and see it's content: 
The content should be something like that:
```
bff_workshop
├── pyproject.toml
├── README.md
├── bff_workshop
│   └── __init__.py
└── tests
    └── __init__.py
```

## Second step - Creating virtual env

In order to create virtual env run `python3 -m venv .venv` after creating your virtual environment you need to activate it by running 
`source .venv/bin/activate` **Try it now!**.

> Don't forget to add `.env` directory to `.gitignore` file!!

### Now we are ready to install some packages :-)

Let's install our packages by running `poetry add fastapi fastapi-sqlalchemy pydantic alembic psycopg2-binary uvicorn`

Now let's see what we installed:

- `fastapi` - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
- `fastapi-sqlalchemy` - FastAPI-SQLAlchemy provides a simple integration between FastAPI and SQLAlchemy in your application. It gives access to useful helpers to facilitate the completion of common tasks.
- `pydantic` - Pydantic is the most widely used data validation library for Python.
- `alembic` - Alembic is a database migrations tool written by the author of SQLAlchemy.
- `psycopg2-binary` - Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
- `uvicorn` - Uvicorn is an ASGI web server implementation for Python.

## Third step - Start coding ...

We will start by creating `main.py` file inside the `bff_workshop` folder (the nested one).
and add the following content to it:

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


def start():
    uvicorn.run("bff_workshop.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["bff_workshop/"],
                reload_delay=1)
```

Now we need to add start script to our project let's add this at the end of our `pyproject.toml` file:

```toml
[tool.poetry.scripts]
start = "bff_workshop.main:start"
```

### We are now ready to run our app :claps:

run `poetry install` and then `poetry run start` and check that everything is running by going to the
url `http://0.0.0.0:9090/health` you spouse to see:
> {"status":"ok"}

# Forth step - Database

Let's add local postgres DB to our project by creating `docker-compose.yml` file with the following content:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:14-alpine
    ports:
      - 5444:5432
    environment:
      - POSTGRES_PASSWORD=S3cret
      - POSTGRES_USER=tikal_user
      - POSTGRES_DB=bff_workshop
```

and then we can lift it up running `docker-compose up -d`

### Yay we have postgres running... 🏃

## Connecting to our DB

Create `.env` file on the root directory and add the following line to it:

```.dotenv
DATABASE_URL="postgresql://tikal_user:S3cret@localhost:5444/bff_workshop"
```

Now we go to our `bff_workshop/main.py` and add the following at the top of the file (after the imports)

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)
```

Now we need to add the following imports:

```python
import os
import sys
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
```
Add this after the `app = FastApi()`
```python
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
```
Now will run in the CLI `alembic init alembic` this will create `alembic` folder and `alembic.ini` file.

In the `alembic.ini` file we change `sqlalchemy.url = driver://user:pass@localhost/dbname` to `sqlalchemy.url =`

In the `alembic/env.py` file we change 

```config = context.config``` 

to 
```BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

config = context.config
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

# Fifth step - CRUD

Our first object we are going to create is `book` so let's create a folder name book and add a file called `orms.py`
inside it.
In this file we will define the SQL schema for book.

```python
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
```

Now we will create a new file in the folder called `models.py` and add this content to it:

```python
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
```

Before we continue we need to create the table in the DB so lets go back to `alembic/env.py` file and add our schema.
We replace `target_metadata = None` with

```python
from bff_workshop.book.orms import BookORM

target_metadata = BookORM.metadata
```

Now we run in our CLI the following command `alembic revision --autogenerate -m "First migration add books table"`
this will create a new file in the `alembic/versions` folder. if it contains our book table we can push it the DB using
the command `alembic upgrade head`

### After so much preparation we can actually start

let's create file named `views.py` inside our `bff_workshop` folder, and put this inside it:

```python
from fastapi import APIRouter

router = APIRouter()
```

Now we can add our first CRUD end point, Let's add this:

```python
from fastapi_sqlalchemy import db
from bff_workshop.book.orms import BookORM


@router.get("")
def get_books_list():
    return db.session.query(BookORM).all()
```

can we use it now? Not yet we need to add the router to the `main.py` file add this the file:

```python
from bff_workshop.book.views import router as book_router

app.include_router(book_router, prefix="/book", tags=["Book"])
```

## Create a book

in order to create a book we will add this code to our `views.py` file:

```python
from bff_workshop.book.models import Book, BookInput


@router.post("")
def create_book(book: BookInput):
    book_orm = BookORM(**book.__dict__)
    db.session.add(book_orm)
    db.session.commit()
    db.session.refresh(book_orm)
    return Book.from_orm(book_orm)
```

We need to create the BookInput in our `models.py` file, we add:

```python

class BookInput(BaseModel):
    title: str
    author: str
```

Now let's run it and check if it works

## Read book

```python
@router.get("/{book_id}")
def get_book(book_id: str):
    return Book.from_orm(db.session.query(BookORM).get(book_id))
```

## Update book

```python
@router.put("/{book_id}")
def update_book(book_id: str, book: BookUpdate):
    book_orm = db.session.query(BookORM).get(book_id)
    for field, value in book.__dict__.items():
        if value is not None:
            setattr(book_orm, field, value)
    db.session.commit()

    return Book.from_orm(book_orm)
```

and in `models.py`

```python
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
```

## Delete book

```python
@router.delete("/{book_id}")
def delete_book(book_id: str):
    db.session.query(BookORM).filter(BookORM.id == book_id).delete()
    db.session.commit()
    return {"status": "success", "message": f"{book_id} deleted successfully!"}
```

### Bonus

> Add type definition to each function to get the api docs more detailed
> `from typing import List, Any, Dict`
> - def get_books_list() -> List[Book]:
> - def create_book(book: BookInput) -> Book:
> - def get_book(book_id: str) -> Book:
> - def update_book(book_id: str, book: BookUpdate) -> Book:
> - def delete_book(book_id: str) -> Dict[str, Any]:
