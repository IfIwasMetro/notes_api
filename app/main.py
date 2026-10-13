from fastapi import FastAPI

from . import models  # noqa: F401  (must be imported so tables are registered on Base)
from .database import Base, engine
from .routers import auth, notes, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notes.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
