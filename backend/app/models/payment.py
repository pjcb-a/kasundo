from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Numeric
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    debt_id = Column(
        Integer,
        ForeignKey("debts.debt_id"),
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    amount_paid = Column(
        Numeric(12, 2),
        nullable=False
    )

    payment_method = Column(
        String(100),
        nullable=False
    )

    notes = Column(
        String(255),
        nullable=True
    )

    paid_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )



    debt = relationship(
        "Debt",
         back_populates="payments"
    )

    creator = relationship(
        "User"
    )