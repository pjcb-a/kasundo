from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password_hash: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    