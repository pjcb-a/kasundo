from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums import DebtRequestStatus

class DebtRequest(Base):
    __tablename__ = "debt_requests"

    request_id = Column(
        Integer, 
        primary_key=True,
        index=True
    )

    lender_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    borrower_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    purpose = Column(
        String(255),
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        Enum(DebtRequestStatus),
        nullable=False,
        default=DebtRequestStatus.PENDING
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    responded_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    acknowledged_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    lender = relationship(
        "User",
        foreign_keys=[lender_id]
    )

    borrower = relationship(
        "User",
        foreign_keys=[borrower_id]
    )

    debt = relationship(
        "Debt",
        back_populates="request",
        uselist=False
    )