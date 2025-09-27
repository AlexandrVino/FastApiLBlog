from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenPairDto:
    access_token: str
    refresh_token: str


@dataclass
class TokenInfoDto:
    subject: str
    expires_in: datetime


@dataclass
class PasswordDto:
    hashed_password: str
    salt: str
