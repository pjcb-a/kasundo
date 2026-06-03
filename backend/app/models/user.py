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
        nullable=False
    )

    phone_number = Column(
        String(20),
        unique=True,
        nullable=False
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

    lent_request = relationship(
        "DebtRequest",
        foreign_keys="DebtRequest.lender_id"
    )
    
    borrowed_request = relationship(
        "DebtRequest",
        foreign_keys="DebtRequest.borrower_id"
    )