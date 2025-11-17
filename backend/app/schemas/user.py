"""
Pydantic schemas for User API validation and serialization.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

from app.models.user import UserTier


# =============================================================================
# User Registration & Authentication
# =============================================================================

class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


# =============================================================================
# User Response Models
# =============================================================================

class UserResponse(BaseModel):
    """Schema for user data in API responses"""
    id: UUID
    email: str
    full_name: Optional[str]
    tier: UserTier
    monthly_uploads_used: int
    uploads_remaining: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithToken(BaseModel):
    """Schema for login response with user data and token"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# =============================================================================
# User Update
# =============================================================================

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    webhook_url: Optional[str] = None
