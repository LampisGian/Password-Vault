import secrets
import string

#This class is responsible for generating strong, random passwords. It uses the secrets module to ensure that the generated 
# passwords are cryptographically secure. The generate_password method creates a password of a specified length 
# (defaulting to 12 characters) that includes a mix of lowercase letters, uppercase letters, digits, and symbols. 
# The method ensures that the generated password contains at least one character from each category and then shuffles the characters 
# to create a random password. The minimum length for the generated password is set to 8 characters to ensure sufficient complexity.
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