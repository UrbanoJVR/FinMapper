from dataclasses import dataclass
from typing import List

from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


@dataclass
class GetAllCategoriesQuery:
    """Empty query"""
    pass


from app.src.application.query_bus_registry import query_handler

@query_handler(GetAllCategoriesQuery)
class GetAllCategoriesQueryHandler:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.get_all()