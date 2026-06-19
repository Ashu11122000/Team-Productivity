from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# User Registration
class UserCreate(BaseModel):
    """
    Request schema for user registration.
    """
    
    email: EmailStr = Field(..., description="Unique user email address", example = ["john.doe@example.com"])
    password: str = Field(..., min_length = 8, max_length = 128, description = "User Password", examples = ["StrongPassword123!"])
    
# User Login
class UserLogin(BaseModel):
    """
    Request schema for user authentication.
    """
    email: EmailStr = Field(..., description = "Registered user email address", examples=["john.doe@example.com"])
    password: str = Field(..., min_length = 8, max_length = 128, description = "User password")
    
# JWT Token Response
class TokenResponse(BaseModel):
    """
    JWT access token response.
    Returned after successful login.
    """
    access_token: str = Field(..., description = "JWT access token")
    token_type: str = Field(default = "bearer", description = "Authentication Scheme", examples = ["bearer"])

# User Profile Response
class UserResponse(BaseModel):
    """
    Standard user response returned to frontend.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description = "Unique user identifier", examples = [1])
    email: EmailStr = Field(..., description = "User email address")
    role: Literal["ADMIN", "MEMBER"] = Field(..., description = "User role", examples = ["MEMBER"])
    is_active: bool = Field(..., description = "User account status", examples = [True])
    created_at: datetime = Field(..., description = "Account creation timestamp")
    updated_at: datetime = Field(..., description = "Last account updated timestamp")
    
# Authenticated User Context
class CurrentUser(BaseModel):
    """
    User context extracted from JWT.
    
    Used internally by:
    - FastAPI authorization
    - RBAC
    - Ownership validation
    - NestJS-compatible JWT payload validation
    """
    
    user_id: int = Field(..., description = "Authenticated user ID")
    email: EmailStr = Field(..., description = "Authenticated user email")
    role: Literal["ADMIN", "MEMBER"] = Field(..., description = "Authenticated user role")

# Shared JWT Payload Contract
class TokenPayload(BaseModel):
    """
    Shared JWT contract between FastAPI and NestJS.
    
    FastAPI:
    - Issues JWT
    
    NestJS:
    - Validates JWT
    """
    sub: str = Field(..., description = "User ID", examples = [1])
    email: EmailStr = Field(..., description = "User email")
    role: Literal["ADMIN", "MEMBER"] = Field(..., description = "User role")
    aud: str = Field(..., description = "JWT audience", examples = ["team-productivity-users"])
    type: str = Field(..., description = "Token type", examples = ["access"])
    exp: int = Field(..., description = "Expiration timestamp")

