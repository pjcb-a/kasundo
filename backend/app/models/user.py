from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(
        Integer, 
        primary_key=True,
        index=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )
    
    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True
    )

    phone_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    profile_picture = Column(
        String,
        nullable=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    last_login = Column(
        DateTime,
        nullable=True
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



    lent_requests = relationship(
        "DebtRequest",
        foreign_keys="DebtRequest.lender_id",
        back_populates="lender"
    )
    
    borrowed_requests = relationship(
        "DebtRequest",
        foreign_keys="DebtRequest.borrower_id",
        back_populates="borrower"
    )

    active_lent_debts = relationship(
    "Debt",
    foreign_keys="Debt.lender_id",
    back_populates="lender"
)

    active_borrowed_debts = relationship(
    "Debt",
    foreign_keys="Debt.borrower_id",
    back_populates="borrower"
)

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    activity_logs = relationship(
        "ActivityLog",
        back_populates="actor"
    )