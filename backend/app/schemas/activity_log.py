from datetime import datetime

from pydantic import BaseModel


class ActivityLogResponse(BaseModel):
    log_id: int
    debt_id: int
    actor_id: int
    action: str
    details: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class ActivityLogSummary(BaseModel):
    action: str

    details: str | None

    created_at: datetime