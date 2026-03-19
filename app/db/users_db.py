"""
Users database access module.

Handles CRUD operations and authentication-related queries for users.
"""

from app.db.create_db import get_connect


def create_users(db, user, hash_password):
        """
        Create a new user in the database.

        Args:
            db: Active database connection.
            user: UserCreate schema.
            hash_password (str): Hashed password.

        Returns:
            int: ID of the created user.
        """

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)""",
            (user.name,
             user.email,
             hash_password
            )
)
        db.commit()
        user_id = cursor.lastrowid

        new_user = get_user_by_id(db, user_id)
        return new_user
    
def get_users(db):
        """
        Retrieve all users.

        Args:
            db: Active database connection.

        Returns:
            list[dict]: List of users.
        """

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    

def get_user_by_id(db, id_user):
        """
        Retrieve a user by ID.

        Args:
            db: Active database connection.
            id_user (int): User ID.

        Returns:
            dict | None: User data or None if not found.
        """

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id_user,))
        
        row = cursor.fetchone()

        if not row:
            return None
        
        return dict(row)
    
def delete_user(db, id_user):
        """
        Delete a user by ID.

        Args:
            db: Active database connection.
            id_user (int): User ID.

        Returns:
            bool: True if deleted, False otherwise.
        """

        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (id_user,))

        db.commit()
        return cursor.rowcount > 0
    
def update_user_patch(db, user_id, user):
    """
    Partially update a user.

    Args:
        db: Active database connection.
        user_id (int): User ID.
        user: UserPatch schema.

    Returns:
        bool: True if updated, False otherwise.
    """

    fields = []
    values = []

    if user.name is not None:
        fields.append("name = ?")
        values.append(user.name)

    if user.email is not None:
        fields.append("email = ?")
        values.append(user.email)
    
    if user.password is not None:
        fields.append("password = ?")
        values.append(user.password)

    values.append(user_id)

    if not fields:
        return False
    
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE users SET {', '.join(fields)} WHERE id = ?", 
        values
    )

    db.commit()

    return cursor.rowcount > 0


def update_total_user(db, id_user, user):
        """
        Fully update a user.

        Args:
            db: Active database connection.
            id_user (int): User ID.
            user: UserCreate schema.

        Returns:
            bool: True if updated, False otherwise.
        """

        cursor = db.cursor()
        cursor.execute("""
            UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?
        """, 
            (
                user.name,
                user.email,
                user.password,
                id_user
            )
     )
        db.commit()

        return cursor.rowcount > 0


def get_user_by_email(db, email):
    """
    Retrieve a user by email.

    Args:
        db: Active database connection.
        email (str): Email address.

    Returns:
        dict | None: User data or None if not found.
    """

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

    row = cursor.fetchone()

    if not row:
        return None
    
    return dict(row)

def update_user_password(db, user_id, password):
    """
    Update a user's password.

    Args:
        db: Active database connection.
        user_id (int): User ID.
        password (str): New hashed password.

    Returns:
        bool: True if updated, False otherwise.
    """

    cursor = db.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))

    db.commit()

    return cursor.rowcount > 0


def update_roles():
    """
    Ensure all users have a role assigned.

    Intended as a migration utility.

    Returns:
        bool: True if any rows were updated.
    """

    with get_connect() as connect:
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET role = 'user' WHERE role is NULL")

        connect.commit()

        return cursor.rowcount > 0

if __name__ == "__main__":
    update_roles()
    print("Roles actualizados")