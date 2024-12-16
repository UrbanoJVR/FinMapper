from typing import List, Sequence

from app.src.domain.category import Category
from app.src.infrastructure.model.category_model import CategoryModel


class CategoryModelMapper:

    @staticmethod
    def map_to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description
        )


    @staticmethod
    def map_to_domain(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description
        )

    def map_model_list_to_class(self, model_list: Sequence[CategoryModel]) -> List[Category]:
        categories: List[Category] = list(map(self.map_to_domain, model_list))
        return categories
