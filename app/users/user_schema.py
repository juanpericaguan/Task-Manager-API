"""
User schemas module.

Defines Pydantic models for user creation, update, and response.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """
    Schema for creating a user.

    Attributes:
        name (str): User name.
        email (EmailStr): Email address.
        password (str): Plain password.
    """

    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schema for user responses.

    Attributes:
        id (int): User ID.
        name (str): User name.
        email (EmailStr): Email.
        role (str): User role.
    """

    id: int
    name: str
    email: EmailStr
    role: str

class UserPatch(BaseModel):
    """
    Schema for partial user updates.

    All fields are optional.
    """

    name : Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    """
    Schema for login credentials (optional use case).

    Attributes:
        email (EmailStr): User email.
        password (str): Password.
    """

    email: EmailStr
    password: str