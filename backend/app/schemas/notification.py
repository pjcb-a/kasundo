from datetime import datetime

from pydantic import BaseModel, Field

from app.enums import NotificationType

from app.schemas.common import ORMBaseSchema



class NotificationResponse(ORMBaseSchema):
    notification_id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime


class NotificationSummary(ORMBaseSchema):
    notification_id: int
    title: str
    type: NotificationType
    is_read: bool
    created_at: datetime