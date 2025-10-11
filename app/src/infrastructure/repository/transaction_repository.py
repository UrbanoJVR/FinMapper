from typing import List

from sqlalchemy import extract, select, delete, func, Integer
from sqlalchemy.orm import Session

from app.src.domain.transaction import Transaction
from app.src.infrastructure.mapper.transaction_model_mapper import (
    map_to_model_list,
    map_to_domain,
    map_to_model, map_to_domain_list,
)
from app.src.infrastructure.repository.model.transaction_model import TransactionModel
from database import db


class TransactionRepository:
    def __init__(self):
        self.session: Session = db.session

    def save_transactions(self, transactions: List[Transaction]):
        transaction_models = map_to_model_list(transactions)
        self.session.add_all(transaction_models)
        self.session.commit()

    def save(self, transaction: Transaction):
        transaction_model = map_to_model(transaction)
        self.session.add(transaction_model)
        self.session.commit()

    def delete_by_id(self, transaction_id: int):
        stmt = delete(TransactionModel).where(TransactionModel.id.__eq__(transaction_id))
        self.session.execute(stmt)
        self.session.commit()

    def update(self, transaction: Transaction):
        transaction_model = map_to_model(transaction)
        self.session.merge(transaction_model)
        self.session.commit()

    def get_by_month_year(self, month: int, year: int) -> List[Transaction]:
        stmt = (
            select(TransactionModel)
            .where(
                extract('month', TransactionModel.date) == month,
                extract('year', TransactionModel.date) == year,
            )
            .order_by(TransactionModel.date.desc())
        )
        result = self.session.execute(stmt).scalars().all()
        return map_to_domain_list(result)

    def get_by_year(self, year: int) -> List[Transaction]:
        stmt = (
            select(TransactionModel)
            .where(extract('year', TransactionModel.date) == year)
            .order_by(TransactionModel.date.desc())
        )
        result = self.session.execute(stmt).scalars().all()
        return map_to_domain_list(result)

    def get_by_month_year_and_category_id(self, month: int, year: int, category_id: int) -> List[Transaction]:
        statement = (
            select(TransactionModel)
            .where(
                extract('month', TransactionModel.date) == month,
                extract('year', TransactionModel.date) == year,
                TransactionModel.category_id.__eq__(category_id)
            )
            .order_by(TransactionModel.date.desc())
        )
        result = self.session.execute(statement).scalars().all()
        return map_to_domain_list(result)

    def get_by_id(self, transaction_id: int) -> Transaction:
        stmt = select(TransactionModel).where(TransactionModel.id.__eq__(transaction_id))
        result = self.session.execute(stmt).scalars().first()
        return map_to_domain(result)

    def get_last_uncategorized(self) -> Transaction:
        stmt = (
            select(TransactionModel)
            .where(TransactionModel.category_id.__eq__(None))
            .order_by(TransactionModel.date.desc())
        )
        result = self.session.execute(stmt).scalars().first()
        return map_to_domain(result)

    def get_uncategorized_by_month_year(self, month: int, year: int) -> List[Transaction]:
        stmt = (
            select(TransactionModel)
            .where(
                extract('month', TransactionModel.date) == month,
                extract('year', TransactionModel.date) == year,
                TransactionModel.category_id.__eq__(None),
            )
            .order_by(TransactionModel.date.desc())
        )
        result = self.session.execute(stmt).scalars().all()
        return map_to_domain_list(result)

    def find_all(self):
        stmt = select(TransactionModel)
        result = self.session.execute(stmt).scalars().all()
        return map_to_domain_list(result)

    def find_first_by_category_id(self, category_id: int) -> Transaction:
        query = select(TransactionModel).where(TransactionModel.category_id.__eq__(category_id))
        return map_to_domain(self.session.execute(query).scalar())

    def count_by_category_id(self, category_id: int) -> int:
        query = select(func.count()).select_from(TransactionModel).where(
            TransactionModel.category_id.__eq__(category_id))
        return self.session.execute(query).scalar()

    def get_years_with_transactions(self) -> list[int]:
        query = (
            select(extract('year', TransactionModel.date).label("year"))
            .distinct()
            .order_by("year")
        )
        result = self.session.execute(query).scalars().all()
        return [int(year) for year in result if year is not None]