import os
import json
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    def __init__(self, config_file: str = "master_config.json"):
        self.config_file = config_file
        self.fernet = None

    def _load_config(self):
        if not os.path.exists(self.config_file):
            return None
        with open(self.config_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_config(self, password_hash: str, salt: bytes):
        data = {
            "password_hash": password_hash,
            "salt": base64.b64encode(salt).decode("utf-8")
        }
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def is_master_password_set(self) -> bool:
        return os.path.exists(self.config_file)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def setup_master_password(self, password: str):
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Master password cannot be empty.")

        salt = os.urandom(16)
        password_hash = self._hash_password(password.strip())
        self._save_config(password_hash, salt)

        key = self._derive_key(password.strip(), salt)
        self.fernet = Fernet(key)

    def unlock(self, password: str) -> bool:
        config = self._load_config()
        if config is None:
            return False

        stored_hash = config["password_hash"]
        provided_hash = self._hash_password(password.strip())

        if not hmac.compare_digest(stored_hash, provided_hash):
            return False

        salt = base64.b64decode(config["salt"].encode("utf-8"))
        key = self._derive_key(password.strip(), salt)
        self.fernet = Fernet(key)
        return True

    def encrypt_password(self, plain_password: str) -> str:
        if self.fernet is None:
            raise ValueError("Vault is locked.")
        return self.fernet.encrypt(plain_password.encode()).decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        if self.fernet is None:
            raise ValueError("Vault is locked.")
        return self.fernet.decrypt(encrypted_password.encode()).decode()

    def change_master_password_config(self, new_password: str):
        if not isinstance(new_password, str) or not new_password.strip():
            raise ValueError("New master password cannot be empty.")

        new_salt = os.urandom(16)
        new_password_hash = self._hash_password(new_password.strip())
        self._save_config(new_password_hash, new_salt)

        new_key = self._derive_key(new_password.strip(), new_salt)
        self.fernet = Fernet(new_key)

    def delete_config(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self.fernet = None