from fastapi import FastAPI

app = FastAPI(
    title="Kasundo API",
    version="1.0.0"
)

app.get("/")
def root():
    return {
        "message": "Kasundo API Running"
    }