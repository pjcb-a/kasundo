from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    debt_id = Column(
        Integer,
        ForeignKey("debts.debt_id"),
        nullable=False
    )

    actor_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    action = Column(
        String(100),
        nullable=False
    )

    details = Column(
        String(500),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )



    debt = relationship(
        "Debt",
        back_populates="activity_logs"
    )

    actor = relationship(
        "User",
        back_populates="activity_logs"
    )