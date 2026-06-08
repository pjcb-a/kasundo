from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    login: str = Field(
        min_length=3,
        max_length=255
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    