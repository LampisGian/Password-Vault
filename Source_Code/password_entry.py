from dataclasses import dataclass
from typing import Optional


@dataclass
class PasswordEntry:
    name: str
    url: str
    username: str
    password: str
    notes: str
    updated_at: str
    entry_id: Optional[int] = None