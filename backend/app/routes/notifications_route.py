from fastapi import APIRouter, Depends
from typing import List 
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.notification import NotificationResponse

from app.services.notification_service import (
    get_my_notifications, mark_notification_as_read,
    mark_all_notifications_as_read
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)



@router.get(
    "",
    response_model=List[NotificationResponse],
    summary="Get My Notifications"
)

def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_my_notifications(
        db=db,
        current_user=current_user
    )



@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Mark Notification As Read"
)

def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return mark_notification_as_read(
        notification_id=notification_id,
        db=db,
        current_user=current_user
    )



@router.patch(
    "/read-all",
    response_model=List[NotificationResponse],
    summary="Mark All Notifications As Read"
)

def read_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return mark_all_notifications_as_read(
        db=db,
        current_user=current_user
    )