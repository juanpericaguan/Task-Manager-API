"""
Database dependency module.

Provides a scoped database connection for each request.
"""

from app.db.create_db import get_connect

def get_db():
    """
    Yield a database connection per request.

    Ensures proper cleanup after request lifecycle.

    Yields:
        sqlite3.Connection: Active database connection.
    """

    db = get_connect()

    try:
        yield db

    finally:
        db.close()

