"""
Tasks database access module.

Contains all CRUD operations related to tasks, including filtering,
pagination, and ownership handling.
"""

def create_task(db, task, owner):
        """
        Insert a new task into the database.

        Args:
            db: Active database connection.
            task: TaskCreate schema instance.
            owner (int): User ID of the task owner.

        Returns:
            dict: Newly created task with owner information.
        """

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date, owner_id)
            VALUES (?, ?, ?, ?, ?)""",
            (
                task.title,
                task.description,
                task.priority,
                task.due_date,
                owner
    )
)
        db.commit()
        task_id = cursor.lastrowid

        new_task = get_task_by_id(db, task_id)
        return new_task
    

def get_all_tasks_db(db, status=None, priority=None, owner_id=None, limit=None, offset=None):
    """
    Retrieve tasks with optional filters and pagination.

    Args:
        db: Active database connection.
        status (str | None): Filter by task status.
        priority (str | None): Filter by priority.
        owner_id (int | None): Filter by owner.
        limit (int | None): Max number of results.
        offset (int | None): Pagination offset.

    Returns:
        list[dict]: List of tasks.
    """

    query = """
            SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, users.id AS owner_id, users.name AS owner_name
            FROM tasks
            JOIN users ON users.id = tasks.owner_id
"""
    filters = []
    values = []

    if status:
        filters.append("status = ?")
        values.append(status)

    if priority:
        filters.append("priority = ?")
        values.append(priority)

    if owner_id:
        filters.append("owner_id = ?")
        values.append(owner_id)


        
    if filters:
        query += " WHERE " + " AND ".join(filters)

    if limit is not None and offset is not None:
        query += "LIMIT ? OFFSET ?"
        values.extend([limit, offset])

    cursor = db.cursor()
    cursor.execute(query, values)

    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row['id'],
            "title": row['title'],
            "description": row['description'],
            "status": row['status'],
            "priority": row['priority'],
            "due_date": row['due_date'],
            "owner": {
                "id": row['owner_id'],
                "name": row['owner_name']
            }
        })

    return tasks
    

def get_task_by_id(db, task_id):
        """
        Retrieve a task by its ID.

        Args:
            db: Active database connection.
            task_id (int): Task ID.

        Returns:
            dict | None: Task data or None if not found.
        """

        cursor =  db.cursor()
        cursor.execute("""
            SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, users.id AS owner_id, users.name AS owner_name
            FROM tasks
            JOIN users ON users.id = tasks.owner_id
            WHERE tasks.id = ?""",
            (task_id,)
    )
        row = cursor.fetchone()

        if not row:
            return None
        
        return {
            "id": row['id'],
            "title": row['title'],
            "description": row['description'],
            "status": row['status'],
            "priority": row['priority'],
            "due_date": row['due_date'],
            "owner": {
                "id": row['owner_id'],
                "name": row['owner_name']
            }
        }
    

def delete_task(db, task_id):
        """
        Delete a task by ID.

        Args:
            db: Active database connection.
            task_id (int): Task ID.

        Returns:
            bool: True if deleted, False otherwise.
        """

        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        db.commit()
        return cursor.rowcount > 0
    
def update_patch_task(db, task_id, task):
    """
    Partially update a task.

    Only provided fields will be updated.

    Args:
        db: Active database connection.
        task_id (int): Task ID.
        task: TaskPatch schema.

    Returns:
        bool: True if updated, False otherwise.
    """

    fields = []
    values = []

    if task.title is not None:
        fields.append("title = ?")
        values.append(task.title)

    if task.description is not None:
        fields.append("description = ?")
        values.append(task.description)

    if task.status is not None:
        fields.append("status = ?")
        values.append(task.status)

    if task.priority is not None:
        fields.append("priority = ?")
        values.append(task.priority)

    if task.due_date is not None:
        fields.append("due_date = ?")
        values.append(task.due_date)

    if task.owner_id is not None:
        fields.append("owner_id = ?")
        values.append(task.owner_id)

    values.append(task_id)

    if not fields:
        return False

    cursor = db.cursor()
    cursor.execute(
        f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", 
        values
    )
    db.commit()
    return cursor.rowcount > 0
    

def update_total_task(db, task_id, task):
        """
        Fully update a task (PUT operation).

        Args:
            db: Active database connection.
            task_id (int): Task ID.
            task: TaskCreate schema.

        Returns:
            bool: True if updated, False otherwise.
        """

        cursor = db.cursor()
        cursor.execute("""
            UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ?, owner_id = ?
            WHERE id = ?""",
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task.due_date,
                task.owner_id,
                task_id
            )
    )
        db.commit()
        return cursor.rowcount > 0
    

    
def get_tasks_by_user(db, user_id):
        """
        Retrieve all tasks belonging to a specific user.

        Args:
            db: Active database connection.
            user_id (int): User ID.

        Returns:
            list[dict]: List of tasks.
        """

        cursor = db.cursor()
        cursor.execute("""
            SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, users.id AS owner_id, users.name AS owner_name
            FROM tasks
            JOIN users ON users.id = tasks.owner_id
            WHERE owner_id = ?""",
            (user_id,)
    )

        rows = cursor.fetchall()

        tasks = []

        for row in rows:
            tasks.append({
                "id": row['id'],
                "title": row['title'],
                "description": row['description'],
                "status": row['status'],
                "priority": row['priority'],
                "due_date": row['due_date'],
                "owner": {
                    "id": row['owner_id'],
                    "name": row['owner_name']
                }
            })

        return tasks