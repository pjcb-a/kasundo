from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.activity_log import ActivityLogResponse

from app.services.activity_log_service import (
    get_my_activity_logs, get_debt_activity_logs
)

from app.enums import ActivityAction



router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"]
)



@router.get(
    "",
    response_model=List[ActivityLogResponse],
    summary="Get My Activity Logs"
)

def get_logs(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    action: ActivityAction | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_activity_logs(
        db=db,
        current_user=current_user,
        limit=limit,
        offset=offset,
        action=action
    )



@router.get(
    "/debt/{debt_id}",
    response_model=List[ActivityLogResponse],
    summary="Get Debt Activity Logs"
)

def get_logs_by_debt(
    debt_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    action: ActivityAction | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_debt_activity_logs(
        debt_id=debt_id,
        db=db,
        current_user=current_user,
        limit=limit,
        offset=offset,
        action=action
    )