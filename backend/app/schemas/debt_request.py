from datetime import date
from datetime import datetime

from pydantic import BaseModel, Field

from app.enums import DebtRequestStatus
from app.schemas.common import ORMBaseSchema

class DebtRequestCreate(BaseModel):
    borrower_id: int = Field(gt=0)
    amount: float = Field(
        gt=0
    )
    purpose: str = Field(
        min_length=3, 
        max_length=255
    )
    due_date: date


class DebtRequestUpdate(BaseModel):
    amount: float | None = Field(
        default=None,
        gt=0
    )
    purpose: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )
    due_date: date | None = None



class DebtRequestReject(BaseModel):
    reason: str | None = Field(
        default=None,
        max_length=255
    )


class DebtRequestResponse(ORMBaseSchema):
    request_id: int
    lender_id: int
    borrower_id: int 
    amount: float
    purpose: str
    due_date: date
    status: DebtRequestStatus
    created_at: datetime
    updated_at: datetime | None
    responded_at: datetime | None
    acknowledged_at: datetime | None



class DebtRequestAccept(BaseModel):
    pass



class DebtRequestSummary(ORMBaseSchema):
    request_id: int
    amount: float
    status: DebtRequestStatus
    due_date: date