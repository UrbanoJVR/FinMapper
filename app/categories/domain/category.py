from dataclasses import dataclass


@dataclass
class Category:
    name: str
    description: str
    id: int = None
