from dataclasses import dataclass


@dataclass
class Category:
    name: str
    description: str | None = None
    id: int | None = None
