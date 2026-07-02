from fastapi import FastAPI
from app.database import Base, engine

from app.routes.auth import ( router as auth_router )
from app.routes.debt_requests_route import ( router as debt_requests_router )
from app.routes.debts_route import ( router as debts_router )
from app.routes.payments_route import ( router as payments_router )
from app.routes.notifications_route import ( router as notifications_router )
from app.routes.activity_logs_route import ( router as activity_logs_router )
from app.routes.dashboard_route import ( router as dashboard_router )

import app.models

app = FastAPI(
    title="Kasundo API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(debt_requests_router)
app.include_router(debts_router)
app.include_router(payments_router)
app.include_router(notifications_router)
app.include_router(activity_logs_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Kasundo API Running"
    }