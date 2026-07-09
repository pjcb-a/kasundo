from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums import ( 
    DebtStatus, NotificationType, 
    ActivityAction
    )

from app.services.notification_service import create_notification
from app.services.activity_log_service import create_activity_log

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
        .with_for_update()
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

    db.add(payment)
    
    debt.remaining_balance -= payment_data.amount_paid

    create_activity_log(
    db=db,
    actor_id=current_user.user_id,
    debt_id=debt.debt_id,
    action=ActivityAction.PAYMENT_RECORDED,
    details=f"User {current_user.user_id} recorded a payment of {payment_data.amount_paid} for Debt {debt.debt_id}."
    )

    create_notification(
    db=db,
    user_id=debt.lender_id,
    notification_type=NotificationType.PAYMENT_RECORDED,
    title="Payment Recorded",
    message="A payment was recorded for your debt."
    )



    if debt.remaining_balance <= 0:
        debt.remaining_balance = 0
        debt.status = DebtStatus.SETTLED
        debt.settled_at = datetime.now(timezone.utc)

        create_notification(
        db=db,
        user_id=debt.lender_id,
        notification_type=NotificationType.DEBT_SETTLED,
        title="Debt Settled",
        message="A debt has been fully settled."
        )

        create_notification(
        db=db,
        user_id=debt.borrower_id,
        notification_type=NotificationType.DEBT_SETTLED,
        title="Debt Settled",
        message="A debt has been fully settled."
        )

        create_activity_log(
        db=db,
        actor_id=current_user.user_id,
        debt_id=debt.debt_id,
        action=ActivityAction.DEBT_SETTLED,
        details=f"Debt {debt.debt_id} was fully settled."
)

    db.commit()
    db.refresh(payment)

    return payment



def get_debt_payments(
    debt_id: int,
    db: Session,
    current_user: User,
    limit: int = 10,
    offset: int = 0
) -> list[Payment]:
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
        .offset(offset)
        .limit(limit)
        .all()
    )