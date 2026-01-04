"""Authentication schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr = Field(description="User's email address")
    password: str = Field(min_length=8, max_length=128, description="Password (min 8 characters)")
    name: str | None = Field(default=None, max_length=100, description="Optional display name")


class SigninRequest(BaseModel):
    """Request schema for user authentication."""

    email: EmailStr = Field(description="User's email address")
    password: str = Field(description="User's password")


class UserResponse(BaseModel):
    """Response schema for user data."""

    id: UUID
    email: str
    name: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
