"""
Task-related dependencies module.

Contains reusable dependencies for task ownership validation.
"""

from fastapi import Depends, HTTPException
from app.db.tasks_db import get_task_by_id
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db

def get_task_owner(
    task_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Validate that the current user owns the specified task.

    Args:
        task_id (int): Task ID.
        db: Database connection.
        current_user (dict): Authenticated user.

    Raises:
        HTTPException: If task does not exist or user is not owner.

    Returns:
        dict: Task data.
    """

    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task['owner']['id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return task
