import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


def start():
    uvicorn.run("bff_workshop.main:app", host="0.0.0.0", port=9090, reload=True, reload_dirs=["bff_workshop/"], reload_delay=1)
