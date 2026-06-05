from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    Date,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums import DebtStatus

class Debt(Base):
    __tablename__ = "debts"

    debt_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    request_id = Column(
        Integer,
        ForeignKey("debt_requests.request_id"),
        unique=True,
        nullable=False
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

    original_amount = Column(
        Numeric(12, 2),
        nullable=False
    )
    
    remaining_balance = Column(
        Numeric(12, 2),
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        Enum(DebtStatus),
        nullable=False,
        default=DebtStatus.ACTIVE
    )

    create_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    settled_at = Column(
        DateTime(timezone=True),
        nullable=True
    )



    request = relationship(
        "DebtRequest",
        back_populates="debt"
    )

    lender = relationship(
        "User",
        foreign_keys=[lender_id]
    )

    borrower = relationship(
        "User",
        foreign_keys=[borrower_id]
    )

    payments = relationship(
        "Payment",
        back_populates="debt",
        cascade="all, delete-orphan"
    )

    activity_logs = relationship(
        "ActivityLog",
        back_populates="debt",
        cascade="all, delete-orphan"
    )