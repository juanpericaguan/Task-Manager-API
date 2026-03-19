"""
Task schemas module.

Defines Pydantic models for task validation, creation, update,
and response serialization.
"""

from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """
    Schema for creating a task.

    Attributes:
        title (str): Task title.
        description (str): Task description.
        priority (Literal): Task priority.
        due_date (datetime): Due date.
    """

    title: str
    description: str
    priority: Literal["low", "standard", "high"]
    due_date: datetime
    

class TaskResponse(BaseModel):
    """
    Schema for task responses.

    Attributes:
        id (int): Task ID.
        title (str): Task title.
        description (str): Description.
        status (Literal): Task status.
        priority (Literal): Priority.
        due_date (datetime): Due date.
        owner (TaskOwner): Owner information.
    """

    id: int
    title: str
    description: str
    status: Literal["pending", "in_progress", "completed"]
    priority: Literal["low", "standard", "high"]
    due_date: datetime
    owner: TaskOwner

class TaskPatch(BaseModel):
    """
    Schema for partial task updates.

    All fields are optional.
    """

    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    owner_id: Optional[int] = None

class TaskOwner(BaseModel):
    """
    Represents task owner information in responses.

    Attributes:
        id (int): User ID.
        name (str): User name.
    """

    id: int
    name: str