from fastapi import APIRouter, Depends, Query
from typing import List, Literal

from sqlalchemy.orm import Session
from app.database import get_db

from app.models.user import User
from app.schemas.debt import DebtResponse
from app.enums import DebtStatus

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
    role: Literal["lender", "borrower"] | None = Query(
        default=None
    ),
    debt_status: DebtStatus | None = Query(
        default=None,
        alias="status"
    ),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_debts(
        db=db,
        current_user=current_user,
        role=role,
        debt_status=debt_status,
        limit=limit,
        offset=offset
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