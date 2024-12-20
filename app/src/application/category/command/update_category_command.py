from dataclasses import dataclass


@dataclass
class UpdateCategoryCommand:
    category_id: int
    category_name: str
    category_description: str
