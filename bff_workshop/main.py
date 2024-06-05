import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from bff_workshop.book.views import router as book_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(book_router, prefix="/book", tags=["Book"])

@app.get("/health")
def health():
    return {"status": "ok"}


def start():
    uvicorn.run("bff_workshop.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["bff_workshop/"], reload_delay=1)
