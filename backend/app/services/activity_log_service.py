from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.debt import Debt
from app.enums import ActivityAction
from app.models.activity_log import ActivityLog
from app.models.user import User



def create_activity_log(
    db: Session,
    actor_id: int,
    action: ActivityAction,
    details: str,
    debt_id: int | None = None
) -> ActivityLog:
    activity_log = ActivityLog(
        actor_id=actor_id,
        debt_id=debt_id,
        action=action,
        details=details
    )

    db.add(activity_log)
    db.flush()

    return activity_log



def get_my_activity_logs(
    db: Session,
    current_user: User,
    limit: int = 10,
    offset: int = 0,
    action: ActivityAction | None = None
) -> list[ActivityLog]:

    query = (
        db.query(ActivityLog)
        .filter(ActivityLog.actor_id == current_user.user_id)
    )

    if action is not None:
        query = query.filter(
            ActivityLog.action == action.value
        )

    return (
        query
        .order_by(ActivityLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )



def get_debt_activity_logs(
    debt_id: int,
    db: Session,
    current_user: User,
    limit: int = 10,
    offset: int = 0,
    action: ActivityAction | None = None
) -> list[ActivityLog]:


    debt = (
        db.query(Debt)
        .filter(Debt.debt_id == debt_id)
        .first()
    )

    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debt not found."
        )

    if current_user.user_id not in [debt.lender_id, debt.borrower_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    query = (
        db.query(ActivityLog)
        .filter(ActivityLog.debt_id == debt_id)
    )

    if action is not None:
        query = query.filter(
            ActivityLog.action == action.value
        )

    return (
        query
        .order_by(ActivityLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

 