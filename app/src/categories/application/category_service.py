from typing import List

from app.src.categories.domain.category import Category
from app.src.categories.infraestructure.category_repository import CategoryRepository


class CategoryService:
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def save_category(self, category: Category):
        self.repository.save(category)

    def delete(self, id: int):
        self.repository.delete(id)

    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> Category:
        return self.repository.get_by_id(id)
