from typing import List

from sqlalchemy import text

from app.src.categories.domain.category import Category
from app.src.categories.infraestructure import category_model_mapper
from app.src.categories.model.category_model import CategoryModel
from database import db


class CategoryRepository:

    def __init__(self):
        pass

    def save(self, category: Category):
        model: CategoryModel = category_model_mapper.map_to_model(category)
        db.session.add(model)
        db.session.commit()

    def delete(self, category_id: int):
        CategoryModel.query.filter_by(id=category_id).delete()
        db.session.commit()

    def update(self, category: Category):
        db.session.merge(category_model_mapper.map_to_model(category))
        db.session.commit()

    def get_all(self) -> List[Category]:
        return category_model_mapper.map_model_list_to_class(CategoryModel.query.all())

    def get_by_id(self, category_id: int) -> Category:
        return category_model_mapper.map_to_entity(CategoryModel.query.filter_by(id=category_id).first())

    def exists_by_name(self, name: str) -> bool:
        if CategoryModel.query.filter_by(name=name).first() is None:
            return False
        else:
            return True

    def get_by_name(self, name: str) -> Category:
        return category_model_mapper.map_to_entity(CategoryModel.query.filter_by(name=name).first())

    def is_category_used(self, category_id: int) -> bool:
        query = f"SELECT COUNT(*) FROM transactions WHERE category_id = {category_id}"
        result = db.session.execute(text(query))
        count = result.scalar()
        return count > 0
