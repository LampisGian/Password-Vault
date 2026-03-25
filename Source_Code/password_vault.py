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

    def is_master_password_set(self) -> bool:
        return self.encryption_manager.is_master_password_set()

    def set_master_password(self, password: str):
        self.encryption_manager.setup_master_password(password)

    def unlock_vault(self, password: str) -> bool:
        return self.encryption_manager.unlock(password)

    def change_master_password(self, old_password: str, new_password: str):
        if not self.encryption_manager.unlock(old_password):
            return False

        rows = self.database_manager.get_all_credentials()
        decrypted_passwords = []

        for row in rows:
            decrypted_passwords.append({
                "id": row[0],
                "password": self.encryption_manager.decrypt_password(row[4])
            })

        self.encryption_manager.change_master_password_config(new_password)

        for item in decrypted_passwords:
            new_encrypted_password = self.encryption_manager.encrypt_password(item["password"])
            self.database_manager.update_encrypted_password(
                item["id"],
                new_encrypted_password,
                self._current_timestamp()
            )

        return True

    def reset_vault(self):
        self.database_manager.delete_database()
        self.encryption_manager.delete_config()

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