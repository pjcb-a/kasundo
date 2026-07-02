from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.dashboard import DashboardSummaryResponse
from app.schemas.payment import PaymentResponse
from app.schemas.activity_log import ActivityLogResponse

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_recent_payments,
    get_recent_activity
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Get Dashboard Summary"
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_summary(
        db=db,
        current_user=current_user
    )


@router.get(
    "/recent-payments",
    response_model=List[PaymentResponse],
    summary="Get Recent Payments"
)
def dashboard_recent_payments(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_recent_payments(
        db=db,
        current_user=current_user,
        limit=limit
    )


@router.get(
    "/recent-activity",
    response_model=List[ActivityLogResponse],
    summary="Get Recent Activity Logs"
)
def dashboard_recent_activity(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_recent_activity(
        db=db,
        current_user=current_user,
        limit=limit
    )