from dataclasses import dataclass
from typing import Optional

#This class represents a password entry in the vault. It is defined as a dataclass for simplicity and ease of use. Each entry contains fields for the name of the credential,
@dataclass
class PasswordEntry:
    name: str
    url: str
    username: str
    password: str
    notes: str
    updated_at: str
    entry_id: Optional[int] = None