from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.enums import DebtStatus, DebtRequestStatus
from app.models.user import User
from app.models.debt import Debt
from app.models.debt_request import DebtRequest
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.activity_log import ActivityLog 



def _to_float(value) -> float:
    return float(value or 0)



def get_dashboard_summary(
    db: Session,
    current_user: User
):

    user_id = current_user.user_id

    total_borrowed_outstanding = (
        db.query(func.coalesce(func.sum(Debt.remaining_balance), 0))
        .filter(Debt.borrower_id == user_id)
        .filter(Debt.status == DebtStatus.ACTIVE)
        .scalar()
    )

    total_lent_outstanding = (
        db.query(func.coalesce(func.sum(Debt.remaining_balance), 0))
        .filter(Debt.lender_id == user_id)
        .filter(Debt.status == DebtStatus.ACTIVE)
        .scalar()
    )

    total_payments_made = (
        db.query(func.coalesce(func.sum(Payment.amount_paid), 0))
        .filter(Payment.created_by == user_id)
        .scalar()
    )

    total_payments_received = (
        db.query(func.coalesce(func.sum(Payment.amount_paid), 0))
        .join(Debt, Payment.debt_id == Debt.debt_id)
        .filter(Debt.lender_id == user_id)
        .scalar()
    )

    active_borrowed_count = (
        db.query(Debt)
        .filter(Debt.borrower_id == user_id)
        .filter(Debt.status == DebtStatus.ACTIVE)
        .count()
    )

    active_lent_count = (
        db.query(Debt)
        .filter(Debt.lender_id == user_id)
        .filter(Debt.status == DebtStatus.ACTIVE)
        .count()
    )

    settled_borrowed_count = (
         db.query(Debt)
        .filter(Debt.borrower_id == user_id)
        .filter(Debt.status == DebtStatus.SETTLED)
        .count()
    )

    settled_lent_count = (
        db.query(Debt)
        .filter(Debt.lender_id == user_id)
        .filter(Debt.status == DebtStatus.SETTLED)
        .count()
    )

    pending_received_requests = (
        db.query(DebtRequest)
        .filter(DebtRequest.borrower_id == user_id)
        .filter(DebtRequest.status == DebtRequestStatus.PENDING)
        .count()
    )

    pending_sent_requests = (
        db.query(DebtRequest)
        .filter(DebtRequest.lender_id == user_id)
        .filter(DebtRequest.status == DebtRequestStatus.PENDING)
        .count()
    )

    unread_notifications_count = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .filter(Notification.is_read == False)
        .count()
    )

    return {
         "total_borrowed_outstanding": _to_float(total_borrowed_outstanding),
        "total_lent_outstanding": _to_float(total_lent_outstanding),

        "total_payments_made": _to_float(total_payments_made),
        "total_payments_received": _to_float(total_payments_received),

        "active_borrowed_count": active_borrowed_count,
        "active_lent_count": active_lent_count,

        "settled_borrowed_count": settled_borrowed_count,
        "settled_lent_count": settled_lent_count,

        "pending_received_requests": pending_received_requests,
        "pending_sent_requests": pending_sent_requests,

        "unread_notifications_count": unread_notifications_count
    }



def get_recent_payments(
    db: Session,
    current_user: User,
    limit: int = 5
):

    return (
        db.query(Payment)
        .join(Debt, Payment.debt_id == Debt.debt_id)
        .filter(
            or_(
                Debt.lender_id == current_user.user_id,
                Debt.borrower_id == current_user.user_id
            )
        )
        .order_by(Payment.paid_at.desc())
        .limit(limit)
        .all()
    )



def get_recent_activity(
    db: Session,
    current_user: User,
    limit: int = 5
):

    return(
        db.query(ActivityLog)
        .filter(ActivityLog.actor_id == current_user.user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )