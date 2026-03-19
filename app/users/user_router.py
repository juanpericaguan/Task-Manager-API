"""
User router module.

Defines user-related endpoints including CRUD operations,
authentication, and role-based access control.
"""

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.db import get_db
from app.users.user_schema import UserCreate, UserResponse, UserPatch, UserLogin
from app.task.task_schema import TaskResponse
from app.db.users_db import (
    create_users, 
    get_users, 
    get_user_by_id, 
    delete_user,
    update_user_patch,
    update_total_user
    )
from app.db.tasks_db import get_tasks_by_user
from app.core.security import (
    hash_password,
    create_access_token,
    )
from app.dependencies.auth import (
    get_current_user, 
    authenticated_user,
    validate_user, 
    require_admin
    )

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ====== ROUTERS CRUD  USERS =========
@router.post(
        "/",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED
    )
def create_user(user: UserCreate, db=Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): User data.
        db: Database connection.

    Returns:
        dict: Created user info.
    """

    hashed_password = hash_password(user.password)
    new_user = create_users(db, user, hashed_password)

    if not new_user:
        raise HTTPException(status_code=422, detail={"Error creating user."})

    return new_user

@router.get(
    "/",
    response_model=list[UserResponse]
)
def show_all_users(required=Depends(require_admin), db=Depends(get_db)):
    """
    Retrieve all users (admin only).

    Args:
        required: Admin validation dependency.
        db: Database connection.

    Returns:
        list[UserResponse]: List of users.
    """

    return get_users(db)



@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_by_id(user_id: int, validated=Depends(validate_user), db=Depends(get_db)):
    """
    Delete a user by ID.

    Args:
        user_id (int): User ID.
        validated: Ownership validation.
        db: Database connection.
    """

    deleted = delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def put_user(user_id: int, user: UserCreate, validated = Depends(validate_user), db=Depends(get_db)):
    """
    Fully update a user.

    Args:
        user_id (int): User ID.
        user (UserCreate): New user data.
        validated: Ownership validation.
        db: Database connection.

    Returns:
        dict: Updated user.
    """

    user.password = hash_password(user.password)
    updated = update_total_user(db, user_id, user)

    if not updated:
        raise HTTPException(status_code=404, detail="User Not found")
    
    get_updated = get_user_by_id(db, user_id)

    return get_updated


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def patch_user(user_id: int, user: UserPatch, validate = Depends(validate_user), db=Depends(get_db)):
    """
    Partially update a user.

    Args:
        user_id (int): User ID.
        user (UserPatch): Fields to update.
        validate: Ownership validation.
        db: Database connection.

    Returns:
        dict: Updated user.
    """

    if user.password is not None:
        user.password = hash_password(user.password)
    updated = update_user_patch(db, user_id, user)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    
    get_updated = get_user_by_id(db, user_id)

    return get_updated


@router.get(
    "/{user_id}/tasks",
    response_model=list[TaskResponse]
)
def get_user_tasks(user=Depends(get_current_user), db=Depends(get_db)):
    """
    Retrieve tasks for the authenticated user.

    Args:
        user (dict): Authenticated user.
        db: Database connection.

    Returns:
        list[TaskResponse]: List of tasks.
    """

    return get_tasks_by_user(db, user['id'])


# ====== VERIFICATION LOGIN ============

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db=Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    Args:
        form_data: OAuth2 login form.
        db: Database connection.

    Returns:
        dict: Access token and token type.
    """


    user = authenticated_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    
    token = create_access_token({"sub": str(user['id'])})

    return {
        "access_token": token,
        "token_type": "bearer"
    }




