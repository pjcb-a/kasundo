from datetime import date, datetime, UTC

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.debt import Debt
from app.models.debt_request import DebtRequest
from app.enums import(
    DebtRequestStatus, DebtStatus
)

from app.schemas.debt_request import DebtRequestCreate
from app.exceptions import (
    BorrowerNotFoundException,
    CannotRequestYourselfException,
    InvalidDueDateException,
    UnauthorizedDebtRequestActionException,
    DebtRequestAlreadyProcessedException,
    DebtRequestNotFoundException
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



def accept_debt_request(
    db: Session,
    request_id: int,
    current_user: User
) -> Debt:

    debt_request = (
        db.query(DebtRequest)
        .filter(
            DebtRequest.request_id == request_id
        )
        .first()
    )

    if not debt_request:
        raise DebtRequestNotFoundException()

    if debt_request.borrower_id != current_user.user_id:
        raise UnauthorizedDebtRequestActionException()

    if debt_request.status != DebtRequestStatus.PENDING:
        raise DebtRequestAlreadyProcessedException()

    debt_request.status = DebtRequestStatus.ACCEPTED
    debt_request.responded_at = datetime.now(UTC)
    debt_request.acknowledged_at = datetime.now(UTC)

    new_debt = Debt(
        request_id=debt_request.request_id,
        lender_id=debt_request.lender_id,
        borrower_id=debt_request.borrower_id,
        purpose=debt_request.purpose,
        original_amount=debt_request.amount,
        remaining_balance=debt_request.amount,
        due_date=debt_request.due_date,
        status=DebtStatus.ACTIVE
    )

    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)

    return new_debt



def reject_debt_request(
    db: Session,
    request_id: int,
    current_user: User
) -> DebtRequest:

    debt_request = (
        db.query(DebtRequest)
        .filter(
            DebtRequest.request_id == request_id
        )
        .first()
    )

    if not debt_request:
        raise DebtRequestNotFoundException()

    if debt_request.borrower_id != current_user.user_id:
        raise UnauthorizedDebtRequestActionException()

    if debt_request.status != DebtRequestStatus.PENDING:
        raise DebtRequestAlreadyProcessedException()

    debt_request.status = DebtRequestStatus.REJECTED
    debt_request.responded_at = datetime.now(UTC)

    db.commit()

    db.refresh(debt_request)

    return debt_request