import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/health")
def health():
    return {"status": "ok"}


def start():
    uvicorn.run("bff_workshop.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["bff_workshop/"], reload_delay=1)
