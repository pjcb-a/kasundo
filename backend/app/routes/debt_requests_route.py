from fastapi import (
    APIRouter, Depends, 
    HTTPException, status
)

from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.debt import DebtResponse
from app.schemas.debt_request import (
    DebtRequestCreate, DebtRequestResponse
)

from app.security import get_current_user
from app.models.user import User

from app.services.debt_request_service import (
    create_debt_request,
    get_sent_requests,
    get_received_requests,
    accept_debt_request,
    reject_debt_request
)

from app.exceptions import (
    BorrowerNotFoundException,
    CannotRequestYourselfException,
    InvalidDueDateException,
    DebtRequestNotFoundException,
    CannotRequestYourselfException,
    InvalidDueDateException,
    DebtRequestNotFoundException,
    UnauthorizedDebtRequestActionException,
    DebtRequestAlreadyProcessedException
)


router = APIRouter(
    prefix="/debt-requests",
    tags=["Debt Requests"]
)

@router.post(
    "",
    response_model=DebtRequestResponse,
    status_code=status.HTTP_201_CREATED
)

def create_request(
    request_data: DebtRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try: 
        return create_debt_request(
            db=db,
            current_user=current_user,
            request_data=request_data
        )

    except BorrowerNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found."
        )

    except CannotRequestYourselfException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot create a debt request for yourself."
        )

    except InvalidDueDateException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Due date must be in the future."
        )



@router.get(
    "/sent",
    response_model=list[DebtRequestResponse]
)

def get_my_sent_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_sent_requests(
        db=db,
        current_user=current_user
    )



@router.get(
    "/received",
    response_model=list[DebtRequestResponse]
)

def get_my_received_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_received_requests(
        db=db,
        current_user=current_user
    )



@router.patch(
    "/{request_id}/accept",
    response_model=DebtResponse
)

def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        return accept_debt_request(
            db=db,
            request_id=request_id,
            current_user=current_user
        )

    except DebtRequestNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debt request not found."
        )

    except UnauthorizedDebtRequestActionException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to accept this request."
        )

    except DebtRequestAlreadyProcessedException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debt request has already been processed."
        )



@router.patch(
    "/{request_id}/reject",
    response_model=DebtRequestResponse
)

def reject_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        return reject_debt_request(
            db=db,
            request_id=request_id,
            current_user=current_user
        )

    except DebtRequestNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debt request not found."
        )

    except UnauthorizedDebtRequestActionException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to reject this request."
        )

    except DebtRequestAlreadyProcessedException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debt request has already been processed."
        )