from fastapi import FastAPI

from app.api import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Welcome to the Parking Flow API"}
