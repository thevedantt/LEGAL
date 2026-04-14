from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Legal Q&A Engine", version="1.0.0")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Legal Q&A Engine API"}