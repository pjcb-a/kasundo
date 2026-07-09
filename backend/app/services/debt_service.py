from sqlalchemy.orm import Session
from sqlalchemy import or_ 
from fastapi import HTTPException, status

from datetime import datetime, UTC
from app.models.debt import Debt
from app.models.user import User
from typing import Literal

from app.enums import (
    DebtStatus, ActivityAction, NotificationType
)

from app.services.activity_log_service import create_activity_log
from app.services.notification_service import create_notification



def get_user_debts(
    db: Session,
    current_user: User,
    role: Literal["lender", "borrower"] | None = None,
    debt_status: DebtStatus | None = None,
    limit: int = 10,
    offset: int = 0
) -> list[Debt]:

    query = db.query(Debt)

    if role == "lender":
        query = query.filter(
            Debt.lender_id == current_user.user_id
        )

    elif role == "borrower":
        query = query.filter(
            Debt.borrower_id == current_user.user_id
        )

    else: 
        query = query.filter(
            or_(
                Debt.lender_id == current_user.user_id,
                Debt.borrower_id == current_user.user_id
            )
        )

    if debt_status is not None:
        query = query.filter(
            Debt.status == debt_status
        )

    return (
        query
        .order_by(Debt.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_debt_by_id(
    debt_id: int,
    db: Session,
    current_user: User
): 
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

    if (
        debt.lender_id != current_user.user_id
        and
        debt.borrower_id != current_user.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this debt."
        )

    return debt



def settle_debt(
    debt_id: int,
    db: Session,
    current_user: User
) -> Debt:
    
    debt = (
        db.query(Debt)
        .filter(Debt.debt_id == debt_id)
        .with_for_update()
        .first()
    )

    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debt not found."
        )

    if debt.lender_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the lender can manually settle this debt."
        )

    if debt.status == DebtStatus.SETTLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debt is already settled."
        )

    try:
        debt.status = DebtStatus.SETTLED
        debt.remaining_balance = 0
        debt.settled_at = datetime.now(UTC)


        create_activity_log(
        db=db,
        actor_id=current_user.user_id,
        debt_id=debt.debt_id,
        action=ActivityAction.DEBT_SETTLED,
        details=(
            f"Lender {current_user.user_id} manually confirmed "
            f"Debt {debt.debt_id} was fully settled."
            )
        )

        create_notification(
            db=db,
            user_id=debt.borrower_id,
            notification_type=NotificationType.DEBT_SETTLED,
            title="Debt Settled",
            message=(
                "The lender manually confirmed that this debt "
                "has been settled."
            ),
        )

        db.commit()
        db.refresh(debt)
        return debt

    except Exception:
        db.rollback()
        raise