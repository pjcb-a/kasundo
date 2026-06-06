from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMBaseSchema

class UserBase(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=100
    )
    last_name: str = Field(
        min_length=2,
        max_length=100
    )
    email: EmailStr
    phone_number: str = Field(
        min_length=11,
        max_length=20
    )

class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    phone_number: str | None = Field(
        default=None,
        min_length=11,
        max_length=20
    )
    profile_picture: str | None = None


class UserResponse(UserBase, ORMBaseSchema):
    user_id: int 
    profile_picture: str | None = None
    is_verified: bool 
    created_at: datetime
    updated_at: datetime
    
