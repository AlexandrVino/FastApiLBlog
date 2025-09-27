from dataclasses import dataclass
from datetime import datetime

from .enums import RoleEnum


@dataclass
class User:
    id: int
    email: str
    is_active: bool
    created_at: datetime

    salt: str
    hashed_password: str
    role: RoleEnum
