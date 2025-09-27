from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    id: int
    title: str
    description: str

    # is not empty only on read operation
    posts: list["Post"] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Post:
    id: int
    body: str
    title: str

    category: Category
    created_at: datetime | None = None
    updated_at: datetime | None = None
