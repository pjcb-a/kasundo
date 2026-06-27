from datetime import datetime

from app.schemas.common import ORMBaseSchema

class ActivityLogResponse(ORMBaseSchema):
    log_id: int
    debt_id: int | None
    actor_id: int
    action: str
    details: str | None
    created_at: datetime

class ActivityLogSummary(ORMBaseSchema):
    action: str
    details: str | None
    created_at: datetime