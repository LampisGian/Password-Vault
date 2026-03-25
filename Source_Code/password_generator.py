import secrets
import string


class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()-_=+[]{};:,.?/"

    def generate_password(self, length: int = 12) -> str:
        if length < 8:
            raise ValueError("Password length must be at least 8.")

        all_characters = self.lowercase + self.uppercase + self.digits + self.symbols

        password_characters = [
            secrets.choice(self.lowercase),
            secrets.choice(self.uppercase),
            secrets.choice(self.digits),
            secrets.choice(self.symbols)
        ]

        for _ in range(length - 4):
            password_characters.append(secrets.choice(all_characters))

        secrets.SystemRandom().shuffle(password_characters)
        return "".join(password_characters)