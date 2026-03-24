import sqlite3
from password_entry import PasswordEntry


class DatabaseManager:
    def __init__(self, db_name: str = "vault.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    notes TEXT,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_credential(self, entry: PasswordEntry):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (name, url, username, password, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.name,
                entry.url,
                entry.username,
                entry.password,
                entry.notes,
                entry.updated_at
            ))
            conn.commit()

    def get_all_credentials(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, url, username, password, notes, updated_at
                FROM passwords
            """)
            return cursor.fetchall()