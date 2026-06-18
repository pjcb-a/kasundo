from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session
from app.database import get_db

from app.models.user import User
from app.schemas.debt import DebtResponse

from app.security import get_current_user

from app.services.debt_service import ( 
    get_user_debts, get_debt_by_id, 
    settle_debt
)


router = APIRouter(
    prefix="/debts",
    tags=["Debts"]
)

@router.get(
    "",
    response_model=List[DebtResponse],
    summary="Get My Debts"
)

def get_my_debts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_debts(
        db=db,
        current_user=current_user
    )



@router.get(
    "/{debt_id}",
    response_model=DebtResponse,
    summary="Get Debt Details"
)

def get_debt(
    debt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_debt_by_id(
        debt_id=debt_id,
        db=db,
        current_user=current_user
    )



@router.patch(
    "/{debt_id}/settle",
    response_model=DebtResponse,
    summary="Settle Debt"
)

def settle_existing_debt(
    debt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return settle_debt(
        debt_id=debt_id,
        db=db,
        current_user=current_user
    )