from typing import List

from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class CategoryService:
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def delete(self, category_id: int):
        if not self.repository.is_category_used(category_id):
            self.repository.delete_by_id(category_id)

    def update(self, category: Category):
        category_on_db: Category = self.repository.get_by_id(category.id)
        if category_on_db is None:
            # Exception
            return None

        self.repository.update(category)
        return category.id

    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> Category:
        return self.repository.get_by_id(id)

    def is_category_used(self, category_id: int) -> bool:
        return self.repository.is_category_used(category_id)
