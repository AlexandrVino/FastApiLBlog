from dataclasses import dataclass, field


@dataclass
class Category:
    id: int
    title: str
    description: str

    # is not empty only on read operation
    posts: list["Post"] = field(default_factory=list)


@dataclass
class Post:
    id: int
    body: str
    title: str

    category: Category
