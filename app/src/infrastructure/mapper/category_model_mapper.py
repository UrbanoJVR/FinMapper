from typing import List, Sequence

from app.src.domain.category import Category
from app.src.infrastructure.model.category_model import CategoryModel


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


def map_model_list_to_class(model_list: Sequence[CategoryModel]) -> List[Category]:
    categories: List[Category] = list(map(map_to_entity, model_list))
    return categories
