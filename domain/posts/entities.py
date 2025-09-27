from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Post:
    id: int
    body: str
    title: str
    created_at: datetime
    updated_at: datetime
    category: Category
