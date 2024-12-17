from typing import List

from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class CategoryService:
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def update(self, category: Category):
        category_on_db: Category = self.repository.get_by_id(category.id)
        if category_on_db is None:
            # Exception
            return None

        self.repository.update(category)
        return category.id
