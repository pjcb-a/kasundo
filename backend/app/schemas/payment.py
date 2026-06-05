from datetime import datetime

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    amount_paid: float
    payment_method: str
    notes: str | None = None


class PaymentResponse(BaseModel):
    payment_id: int
    debt_id: int
    created_by: int
    amount_paid: float
    payment_method: str
    notes: str | None
    paid_at: datetime

    class Config:
        from_attributes = True


class PaymentSummary(BaseModel):
    payment_id: int
    amount_paid: float
    paid_at: datetime