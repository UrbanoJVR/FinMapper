from typing import List

from app.categories.domain.category import Category
from app.categories.infraestructure.category_repository import CategoryRepository


class CategoryService:

    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def save_category(self, category: Category):
        self.repository.save(category)

    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all()