"""
Authentication dependencies module.

Contains reusable FastAPI dependencies for authentication,
authorization, and user validation.
"""

from fastapi import HTTPException, Depends
from app.core.security import hash_password, verify_password, decode_access_token, oauth2_schema
from app.dependencies.db import get_db
from app.db.users_db import get_user_by_id, get_user_by_email, update_user_password
import hashlib


def get_current_user(
    token: str = Depends(oauth2_schema),
    db=Depends(get_db)
):
    """
    Retrieve the currently authenticated user from JWT token.

    Args:
        token (str): JWT token extracted via OAuth2 scheme.
        db: Database dependency.

    Raises:
        HTTPException: If token is invalid or user does not exist.

    Returns:
        dict: Authenticated user.
    """

    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    
    user_id = int(payload.get("sub"))

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return user


def validate_user(
    user_id: int,
    user=Depends(get_current_user)
):
    """
    Ensure that the authenticated user matches the requested user ID.

    Args:
        user_id (int): Target user ID.
        user (dict): Authenticated user.

    Raises:
        HTTPException: If user is not authorized.

    Returns:
        dict: Validated user.
    """

    if not user['id'] == user_id:
        raise HTTPException(status_code=401, detail="User unauthorized for this action")
    return user


def authenticated_user(db, email: str, password:str):
    """
    Authenticate user credentials.

    Supports migration from SHA256 to bcrypt by re-hashing
    legacy passwords on successful login.

    Args:
        db: Database connection.
        email (str): User email.
        password (str): Plain password.

    Returns:
        dict | None: Authenticated user or None if invalid.
    """

    user = get_user_by_email(db, email)

    if not user:
        return None

    stored_password = user['password']

    # bcrypt flow
    if stored_password.startswith('$2b$'):
        if not verify_password(password, stored_password):
            return None
        return user
    
    # legacy SHA256 flow
    hashlib_ok = hashlib.sha256(password.encode()).hexdigest() == stored_password

    if not hashlib_ok:
        return None
    
    # migrate to bcrypt
    new_hash = hash_password(password)
    update_user_password(db, user['id'], new_hash)

    return user


def require_admin(user=Depends(get_current_user)):
    """
    Restrict access to admin users only.

    Args:
        user (dict): Authenticated user.

    Raises:
        HTTPException: If user is not admin.

    Returns:
        dict: Authenticated admin user.
    """

    if user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    
    return user