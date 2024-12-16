from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import text, delete, select

from app.src.domain.category import Category
from app.src.infrastructure.mapper import category_model_mapper
from app.src.infrastructure.mapper.category_model_mapper import CategoryModelMapper
from app.src.infrastructure.model.category_model import CategoryModel
from database import db


class CategoryRepository:
    def __init__(self):
        self.session: Session = db.session
        self.category_model_mapper = CategoryModelMapper()

    def save(self, category: Category):
        model: CategoryModel = self.category_model_mapper.map_to_model(category)
        self.session.add(model)
        self.session.commit()

    def delete_by_id(self, category_id: int):
        query = delete(CategoryModel).where(CategoryModel.id.__eq__(category_id))
        self.session.execute(query)
        self.session.commit()

    def update(self, category: Category):
        self.session.merge(self.category_model_mapper.map_to_model(category))
        self.session.commit()

    def get_all(self) -> List[Category]:
        query = select(CategoryModel).order_by(CategoryModel.id)
        return self.category_model_mapper.map_model_list_to_class(self.session.execute(query).scalars().all())

    def get_by_id(self, category_id: int) -> Category:
        query = select(CategoryModel).where(CategoryModel.id.__eq__(category_id))
        return self.category_model_mapper.map_to_domain(self.session.execute(query).scalars().first())

    def exists_by_name(self, name: str) -> bool:
        query = select(CategoryModel).where(CategoryModel.name.__eq__(name))
        if self.session.execute(query).first() is None:
            return False
        else:
            return True

    def get_by_name(self, name: str) -> Category:
        query = select(CategoryModel).where(CategoryModel.name.__eq__(name))
        return self.category_model_mapper.map_to_domain(self.session.execute(query).scalar())

    def is_category_used(self, category_id: int) -> bool:
        # TODO pensar refactor para no mezclar responsabilidades en repos
        query = f"SELECT COUNT(*) FROM transactions WHERE category_id = {category_id}"
        result = self.session.execute(text(query))
        count = result.scalar()
        return count > 0
