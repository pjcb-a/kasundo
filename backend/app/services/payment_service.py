from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums import DebtStatus
from app.models.debt import Debt
from app.models.payment import Payment
from app.models.user import User
from app.schemas.payment import ( PaymentCreate )



def record_payment(
    debt_id: int,
    payment_data: PaymentCreate,
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

    if debt.borrower_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the borrower can record payments."
        )

    if debt.status == DebtStatus.SETTLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debt is already settled."
        )

    if payment_data.amount_paid > debt.remaining_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment exceeds remaining balance."
        )



    payment = Payment(
        debt_id=debt.debt_id,
        created_by=current_user.user_id,
        amount_paid=payment_data.amount_paid,
        payment_method=payment_data.payment_method,
        notes=payment_data.notes
    )

    debt.remaining_balance -= payment_data.amount_paid

    if debt.remaining_balance <= 0:
        debt.remaining_balance = 0
        debt.status = DebtStatus.SETTLED
        debt.settled_at = datetime.now(timezone.utc)

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment



def get_debt_payments(
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
        current_user.user_id
        not in [
            debt.lender_id,
            debt.borrower_id
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return (
        db.query(Payment)
        .filter(Payment.debt_id == debt_id)
        .order_by(Payment.paid_at.desc())
        .all()
    )