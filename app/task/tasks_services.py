"""
Task services module.

Contains business logic for tasks, acting as an abstraction layer
between routers and database access.
"""

from app.db.tasks_db import get_all_tasks_db

def get_tasks_service(db, status, priority, owner_id, limit, offset):
    """
    Retrieve tasks applying business rules.

    Includes validation for pagination limits.

    Args:
        db: Database connection.
        status (str | None): Filter by status.
        priority (str | None): Filter by priority.
        owner_id (int): Owner ID.
        limit (int): Max results.
        offset (int): Pagination offset.

    Returns:
        list[dict]: List of tasks.
    """

    if not 0 < limit <= 100:
        limit = 100

    return get_all_tasks_db(db, status, priority, owner_id, limit, offset)