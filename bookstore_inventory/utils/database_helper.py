import sqlite3
from pathlib import Path


class DatabaseHelper:
    """Basic local SQLite helper class for bookstore data."""

    def __init__(self, db_name='bookstore_local.db'):
        self.db_path = Path(db_name)

    def connection(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):
        with self.connection() as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS inventory_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    changed_at TEXT NOT NULL
                )
                '''
            )
