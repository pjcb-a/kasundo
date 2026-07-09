from fastapi import HTTPException, status 
from sqlalchemy.orm import Session

from app.enums import NotificationType
from app.models.notification import Notification
from app.models.user import User 

def create_notification(
    db: Session,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    message: str 
) -> Notification: 
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message
    )

    db.add(notification)
    db.flush()

    return notification



def get_my_notifications(
    db: Session, 
    current_user: User,
    limit: int = 10,
    offset: int = 0,
    is_read: bool | None = None
) -> list[Notification]:

    query = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.user_id)
    )

    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)

    return (
        query
        .order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )



def mark_notification_as_read(
    notification_id: int,
    db: Session,
    current_user: User
) -> Notification:
    notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found."
        )

    if notification.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this notification."
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification



def mark_all_notifications_as_read(
    db: Session,
    current_user: User
) -> list[Notification]:
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.user_id)
        .filter(Notification.is_read == False)
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return notifications



def get_unread_notifications_count(
    db: Session,
    current_user: User
) -> int:
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.user_id)
        .filter(Notification.is_read == False)
        .count()
    )