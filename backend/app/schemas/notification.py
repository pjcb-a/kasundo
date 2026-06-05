from datetime import datetime

from pydantic import BaseModel

from app.enums import NotificationType


class NotificationMarkRead(BaseModel):
    is_read: boll=True


class NotificationResponse(BaseModel):
    notification_id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime

    class Config: 
        from_attributes = True

class NotificationSummary(BaseModel):
    notification_id: int
    title: str
    type: NotificationType
    is_read: bool
    created_at: datetime