"""
Database connection and initialization module.

Handles SQLite connection creation and schema setup.
"""
import sqlite3 as sq

DB_NAME = "task_manager.db"


def get_connect():
    """
    Create a new database connection.

    Returns:
        sqlite3.Connection: Database connection with row factory enabled.
    """
    connect = sq.connect(DB_NAME)
    connect.row_factory = sq.Row
    return connect


def create_table():
    """
    Create database tables if they do not exist.

    Includes users and tasks tables with constraints and relationships.
    """
    with get_connect() as connect:
        cursor = connect.cursor()
        cursor.execute("PRAGMA foreign_key = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
    )
""")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ('pending', 'in_progress', 'completed')),
                priority TEXT NOT NULL
                    CHECK(priority IN ('low', 'standard', 'high')),
                due_date TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")
        connect.commit()


def add_column_role():
    """
    Add role column to users table.

    Intended for migration purposes.
    """
    with get_connect() as connect:
        cursor = connect.cursor()
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        connect.commit()


if __name__ == "__main__":
    create_table()
    print("Database initialized successfully.")