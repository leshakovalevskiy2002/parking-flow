from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {"message": "Welcome to the Parking Flow API"}
