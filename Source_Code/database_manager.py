import os
import sqlite3
from password_entry import PasswordEntry

#This class is responsible for managing the SQLite database that stores the password entries. It provides methods to create the database, 
# add , retrieve, update, and delete credentials. The database is stored in a file named "vault.db" by default, but this can be customized when 
#initializing the DatabaseManager.

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
                ORDER BY id
            """)
            return cursor.fetchall()

    def search_credentials(self, query: str):
        with self._connect() as conn:
            cursor = conn.cursor()
            like_query = f"%{query}%"
            cursor.execute("""
                SELECT id, name, url, username, password, notes, updated_at
                FROM passwords
                WHERE name LIKE ? OR url LIKE ? OR username LIKE ? OR notes LIKE ?
                ORDER BY id
            """, (like_query, like_query, like_query, like_query))
            return cursor.fetchall()

    def get_credential_by_id(self, entry_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, url, username, password, notes, updated_at
                FROM passwords
                WHERE id = ?
            """, (entry_id,))
            return cursor.fetchone()

    def update_credential(self, entry_id: int, entry: PasswordEntry) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE passwords
                SET name = ?, url = ?, username = ?, password = ?, notes = ?, updated_at = ?
                WHERE id = ?
            """, (
                entry.name,
                entry.url,
                entry.username,
                entry.password,
                entry.notes,
                entry.updated_at,
                entry_id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def update_encrypted_password(self, entry_id: int, encrypted_password: str, updated_at: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE passwords
                SET password = ?, updated_at = ?
                WHERE id = ?
            """, (encrypted_password, updated_at, entry_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_credential(self, entry_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
            conn.commit()
            return cursor.rowcount > 0

    def delete_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self._create_table()