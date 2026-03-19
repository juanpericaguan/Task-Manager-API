"""
Security utilities module.

Provides helper functions for password hashing, verification,
and JWT token creation/validation.
"""
from datetime import datetime, timedelta
import bcrypt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MIN
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

# OAuth2 scheme used for token extraction from requests
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed one.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict) -> str:
    """
    Generate a JWT access token.

    Args:
        data (dict): Payload data to encode.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """
    Decode a JWT token.

    Args:
        token (str): JWT token.

    Returns:
        dict | None: Decoded payload or None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None