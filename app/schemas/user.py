from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# -----------------------------
# User Registration Request
# -----------------------------
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)


# -----------------------------
# User Login Request
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# User Response
# -----------------------------
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime
    phone_number: str
    is_active: bool

    class Config:
        from_attributes = True


# -----------------------------
# JWT Token Response
# -----------------------------
class Token(BaseModel):
    access_token: str
    token_type: str