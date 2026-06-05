from datetime import date
from datetime import datetime

from pydantic import BaseModel

from app.enums import DebtStatus


class DebtResponse(BaseModel):
    debt_id: int
    request_id: int
    lender_id: int
    borrower_id: int
    original_amount: float
    remaining_balance: float
    due_date: date
    status: DebtStatus
    created_at: datetime
    updated_at: datetime | None
    settled_at: datetime | None
    
    class Config: from_attributes = True


class DebtSummary(BaseModel):
    debt_id: int
    original_amount: float
    remaining_balance: float
    due_date: date
    status: DebtStatus