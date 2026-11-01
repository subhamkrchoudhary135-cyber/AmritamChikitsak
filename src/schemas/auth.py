"""Authentication and User schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.core.security import UserRole


class UserRegister(BaseModel):
    """User registration payload."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.PATIENT

    # Patient identity fields for immediate profile creation if role=patient
    full_name: str | None = Field(None, min_length=2, max_length=100)
    phone_number: str | None = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    abha_id: str | None = Field(None, description="Ayushman Bharat Health Account 14-digit ID")
    age: int | None = Field(None, ge=1, le=120)
    gender: str | None = Field("other", pattern="^(male|female|other)$")
    preferred_language: str | None = Field("en", pattern="^(en|hi|pa)$")


class UserLogin(BaseModel):
    """Login credentials payload."""

    username: str
    password: str


class Token(BaseModel):
    """JWT bearer token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    expires_in: int


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    sub: str
    role: str
    exp: int
    iat: int
    type: str


class RefreshTokenRequest(BaseModel):
    """Refresh token payload."""

    refresh_token: str


class UserResponse(BaseModel):
    """Public user response."""

    id: str
    email: EmailStr
    username: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
