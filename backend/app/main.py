from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.database import Base, engine
import app.models

app = FastAPI(
    title="Kasundo API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Kasundo API Running"
    }