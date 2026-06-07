from fastapi import FastAPI
from app.routes.auth import router as auth_router



app = FastAPI(
    title="Kasundo API",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Kasundo API Running"
    }