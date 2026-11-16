from fastapi import FastAPI

from app.api import router
from app.config.exceptions import setup_exception_handlers

app = FastAPI()

setup_exception_handlers(app)

app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Welcome to the Parking Flow API"}
