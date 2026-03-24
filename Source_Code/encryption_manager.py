from cryptography.fernet import Fernet
import os


class EncryptionManager:
    def __init__(self, key_file: str = "secret.key"):
        self.key_file = key_file
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)

    def _load_or_create_key(self) -> bytes:
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()

        key = Fernet.generate_key()
        with open(self.key_file, "wb") as file:
            file.write(key)

        return key

    def encrypt_password(self, plain_password: str) -> str:
        encrypted = self.fernet.encrypt(plain_password.encode())
        return encrypted.decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        decrypted = self.fernet.decrypt(encrypted_password.encode())
        return decrypted.decode()