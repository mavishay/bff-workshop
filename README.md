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

In order to create a new python project got the directory you want to create your project in using the CLI and run `poetry new bff-workshop`
This will create new folder with several files. **Try it now!**. 

If everything worked as planned it should have return you this message 
> Created package bff-workshop in bff-workshop

Let's open the new created folder with a code editor and see it's content: 
The content should be something like that:
```
bff-workshop
├── pyproject.toml
├── README.md
├── bff-workshop
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

We will start by creating `main.py` file inside the `bff-workshop` folder (the nested one).
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


