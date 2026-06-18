from sqlalchemy.orm import Session
from sqlalchemy import or_ 
from fastapi import HTTPException, status

from datetime import datetime, UTC
from app.models.debt import Debt
from app.models.user import User

from app.enums import DebtStatus



def get_user_debts(
    db: Session,
    current_user: User
):
    return (
        db.query(Debt)
        .filter(
            or_(
                Debt.lender_id == current_user.user_id,
                Debt.borrower_id == current_user.user_id
            )
        )
        .order_by(Debt.created_at.desc())
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
            detail="You are not allowed to settle this debt."
        )

    if debt.status == DebtStatus.SETTLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debt is already settled."
        )

    debt.status = DebtStatus.SETTLED
    debt.remaining_balance = 0
    debt.settled_at = datetime.now(UTC)

    db.commit()
    db.refresh(debt)

    return debt