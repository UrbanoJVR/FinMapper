from typing import List

from app import db
from app.src.categories.domain.category import Category
from app.src.categories.infraestructure import category_model_mapper
from app.src.categories.model.category_model import CategoryModel


class CategoryRepository:

    def __init__(self):
        pass

    def save(self, category: Category):
        model: CategoryModel = category_model_mapper.map_to_model(category)
        db.session.add(model)
        db.session.commit()

    def get_all(self) -> List[Category]:
        return category_model_mapper.map_model_list_to_class(CategoryModel.query.all())

    def get_by_id(self, id: int) -> Category:
        return category_model_mapper.map_to_class(CategoryModel.query.filter_by(id=id).first())
