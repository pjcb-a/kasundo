from datetime import datetime

from decimal import Decimal
from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseSchema


class PaymentCreate(BaseModel):
    amount_paid: Decimal = Field(
        gt=0
    )
    payment_method: str = Field(
        min_length=2,
        max_length=100
    )
    notes: str | None = Field(
        default=None,
        max_length=255
    )



class PaymentResponse(ORMBaseSchema):
    payment_id: int
    debt_id: int
    created_by: int
    amount_paid: Decimal
    payment_method: str
    notes: str | None
    paid_at: datetime



class PaymentSummary(ORMBaseSchema):
    payment_id: int
    amount_paid: Decimal
    paid_at: datetime