from dataclasses import dataclass
from typing import List

from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class GetAllCategoriesQueryHandler:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.get_all()

@dataclass
class GetAllCategoriesQuery:
    """Empty query"""
    pass