from datetime import datetime
from password_entry import PasswordEntry
from encryption_manager import EncryptionManager
from database_manager import DatabaseManager


class PasswordVault:
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.database_manager = DatabaseManager()

    def _current_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _validate_required_text(self, value: str, field_name: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    def _validate_entry_id(self, entry_id: int):
        if not isinstance(entry_id, int) or entry_id <= 0:
            raise ValueError("Invalid entry ID.")

    def add_entry(self, name: str, url: str, username: str, password: str, notes: str):
        self._validate_required_text(name, "Name")
        self._validate_required_text(username, "Username")
        self._validate_required_text(password, "Password")

        encrypted_password = self.encryption_manager.encrypt_password(password)

        entry = PasswordEntry(
            name=name.strip(),
            url=url.strip(),
            username=username.strip(),
            password=encrypted_password,
            notes=notes.strip(),
            updated_at=self._current_timestamp()
        )

        self.database_manager.add_credential(entry)

    def retrieve_entries(self):
        rows = self.database_manager.get_all_credentials()
        entries = []

        for row in rows:
            entry = {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "username": row[3],
                "password": self.encryption_manager.decrypt_password(row[4]),
                "notes": row[5],
                "updated_at": row[6]
            }
            entries.append(entry)

        return entries

    def get_entry_by_id(self, entry_id: int):
        self._validate_entry_id(entry_id)
        row = self.database_manager.get_credential_by_id(entry_id)

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "url": row[2],
            "username": row[3],
            "password": self.encryption_manager.decrypt_password(row[4]),
            "notes": row[5],
            "updated_at": row[6]
        }

    def update_entry(self, entry_id: int, name: str, url: str, username: str, password: str, notes: str) -> bool:
        self._validate_entry_id(entry_id)
        self._validate_required_text(name, "Name")
        self._validate_required_text(username, "Username")
        self._validate_required_text(password, "Password")

        encrypted_password = self.encryption_manager.encrypt_password(password)

        entry = PasswordEntry(
            name=name.strip(),
            url=url.strip(),
            username=username.strip(),
            password=encrypted_password,
            notes=notes.strip(),
            updated_at=self._current_timestamp()
        )

        return self.database_manager.update_credential(entry_id, entry)

    def delete_entry(self, entry_id: int) -> bool:
        self._validate_entry_id(entry_id)
        return self.database_manager.delete_credential(entry_id)