from datetime import datetime
from password_entry import PasswordEntry
from encryption_manager import EncryptionManager
from database_manager import DatabaseManager


class PasswordVault:
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.database_manager = DatabaseManager()

    def add_entry(self, name: str, url: str, username: str, password: str, notes: str):
        encrypted_password = self.encryption_manager.encrypt_password(password)
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = PasswordEntry(
            name=name,
            url=url,
            username=username,
            password=encrypted_password,
            notes=notes,
            updated_at=updated_at
        )

        self.database_manager.add_credential(entry)