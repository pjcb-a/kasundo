from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserBase):
    first_name: str | None = none
    last_name: str | None = none
    phone_number: str | None = none
    profile_picture: str | None = none 


class UserResponse(UserBase):
    user_id: int 
    profile_picture: str | None = none
    is_verified: bool 
    create_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
