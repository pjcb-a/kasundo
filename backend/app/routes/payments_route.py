from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.payment import (
    PaymentCreate, PaymentResponse
)

from app.services.payment_service import (
    record_payment, get_debt_payments
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)



@router.post(
    "/debt/{debt_id}",
    response_model=PaymentResponse
)

def create_payment(
    debt_id: int,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return record_payment(
         debt_id=debt_id,
        payment_data=payment_data,
        db=db,
        current_user=current_user
    )



@router.get(
    "/debt/{debt_id}",
    response_model=List[PaymentResponse]
)

def get_payment_history(
    debt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_debt_payments(
        debt_id=debt_id,
        db=db,
        current_user=current_user
    )