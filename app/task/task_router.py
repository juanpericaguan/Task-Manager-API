"""
Task router module.

Defines all task-related API endpoints including CRUD operations
and integrates dependencies for authentication and authorization.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.dependencies.db import get_db
from app.task.tasks_services import get_tasks_service
from app.task.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskPatch
)
from app.db.tasks_db import (
    create_task,
    get_task_by_id,
    delete_task,
    update_patch_task,
    update_total_task
)
from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.task_dependencies import get_task_owner

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# ====== ROUTERS CRUD TASKS ========

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_tasks(task: TaskCreate, owner=Depends(get_current_user), db=Depends(get_db)):
    """
    Create a new task for the authenticated user.

    Args:
        task (TaskCreate): Task data.
        owner (dict): Authenticated user.
        db: Database connection.

    Returns:
        dict: Created task.
    """

    new_task = create_task(db, task, owner['id'])

    if not new_task:
        raise HTTPException(status_code=422, detail="Error creating task")
    
    return new_task

@router.get(
    "/",
    response_model=list[TaskResponse]
)
def get_tasks(
    status: str | None= None,
    priority: str | None = None,
    limit: int = 10,
    offset: int = 0,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Retrieve tasks for the authenticated user with optional filters.

    Args:
        status (str | None): Filter by status.
        priority (str | None): Filter by priority.
        limit (int): Max number of tasks.
        offset (int): Pagination offset.

    Returns:
        list[TaskResponse]: List of tasks.
    """

    return get_tasks_service(
        db, 
        status=status, 
        priority=priority, 
        owner_id=current_user['id'], 
        limit=limit, 
        offset=offset
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_tasks(task_id: int, task=Depends(get_task_owner), db=Depends(get_db)):
    """
    Delete a task owned by the authenticated user.

    Args:
        task (dict): Validated task.
        db: Database connection.
    """

    deleted = delete_task(db, task_id)

    

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def put_task(task_data: TaskCreate, db=Depends(get_db), task = Depends(get_task_owner)):
    """
    Fully update a task (replace all fields).

    Args:
        task_data (TaskCreate): New task data.
        db: Database connection.
        task (dict): Existing task.

    Returns:
        dict: Updated task.
    """

    updated = update_total_task(db, task['id'], task_data)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    get_update = get_task_by_id(db, task['id'])

    return get_update


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
def patch_task(task_data: TaskPatch, db=Depends(get_db), task = Depends(get_task_owner)):
    """
    Partially update a task.

    Args:
        task_data (TaskPatch): Fields to update.
        db: Database connection.
        task (dict): Existing task.

    Returns:
        dict: Updated task.
    """

    updated = update_patch_task(db, task['id'], task_data)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    get_updated = get_task_by_id(db, task['id'])

    return get_updated