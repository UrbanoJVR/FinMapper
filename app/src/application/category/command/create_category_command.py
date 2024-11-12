from dataclasses import dataclass


@dataclass
class CreateCategoryCommand:
    name: str
    description: str