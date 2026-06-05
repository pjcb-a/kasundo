from datetime import date
from datetime import datetime

from pydantic import BaseModel

from app.enums import DebtRequestStatus

class DebtRequestCreate(BaseModel):
    borrower_id: int
    amount: float
    purpose: str
    due_date: date


class DebtRequestUpdate(BaseModel):
    amount: float | None = None
    purpose: str | None = None
    due_date: date | None = None


class DebtRequestAccept(BaseModel):
    pass 


class DebtRequestReject(BaseModel):
    reason: str | None = None


class DebtRequestResponse(BaseModel):
    request_id: int
    lender_id: int
    borrower_id: int 
    amount: float
    purpose: str
    due_date: date
    status: DebtRequestStatus
    created_at: datetime
    updated_at: datetime
    responded_at: datetime
    acknowledged_at: datetime

    class Config:
        from_attributes = True