from datetime import date

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.debt_request import DebtRequest

from app.schemas.debt_request import DebtRequestCreate
from app.exceptions import (
    BorrowerNotFoundException,
    CannotRequestYourselfException,
    InvalidDueDateException
)



def create_debt_request(
    db: Session,
    current_user: User,
    request_data: DebtRequestCreate
) -> DebtRequest:

    borrower = (
        db.query(User)
        .filter(
            User.user_id == request_data.borrower_id    
        )
        .first()
    )

    if not borrower:
        raise BorrowerNotFoundException()

    if borrower.user_id == current_user.user_id:
        raise CannotRequestYourselfException()

    if request_data.due_date <= date.today():
        raise InvalidDueDateException()

    debt_request = DebtRequest(
        lender_id=current_user.user_id,
        borrower_id=request_data.borrower_id,
        amount=request_data.amount,
        purpose=request_data.purpose,
        due_date=request_data.due_date
    )

    db.add(debt_request)
    db.commit()
    db.refresh(debt_request)

    return debt_request



def get_sent_requests(
    db: Session,
    current_user: User
) -> list[DebtRequest]:
    
    return (
        db.query(DebtRequest)
        .filter(
            DebtRequest.lender_id
            == current_user.user_id
        )
        .order_by(
            DebtRequest.created_at.desc()
        )
        .all()
    )



def get_received_requests(
    db: Session,
    current_user: User
) -> list[DebtRequest]:

      return (
        db.query(DebtRequest)
        .filter(
            DebtRequest.borrower_id
            == current_user.user_id
        )
        .order_by(
            DebtRequest.created_at.desc()
        )
        .all()
    )

