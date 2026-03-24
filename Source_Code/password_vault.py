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

    def retrieve_entries(self):
        rows = self.database_manager.get_all_credentials()
        entries = []

        for row in rows:
            decrypted_password = self.encryption_manager.decrypt_password(row[4])

            entry = {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "username": row[3],
                "password": decrypted_password,
                "notes": row[5],
                "updated_at": row[6]
            }

            entries.append(entry)

        return entries