from typing import List

from app.src.categories.domain.category import Category
from app.src.categories.model.category_model import CategoryModel


def map_to_model(category: Category) -> CategoryModel:
    return CategoryModel(
        id=category.id,
        name=category.name,
        description=category.description
    )


def map_to_entity(model: CategoryModel) -> Category:
    return Category(
        id=model.id,
        name=model.name,
        description=model.description
    )


def map_model_list_to_class(model_list: List[CategoryModel]) -> List[Category]:
    categories: List[Category] = list(map(map_to_entity, model_list))
    return categories
