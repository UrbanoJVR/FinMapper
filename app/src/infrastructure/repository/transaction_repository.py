from typing import List

from sqlalchemy import extract

from app.src.domain.transaction import Transaction
from app.src.infrastructure.mapper.transaction_model_mapper import map_to_model_list, \
    map_to_entity_list, map_to_domain, map_to_model
from app.src.infrastructure.model.transaction_model import TransactionModel
from database import db


class TransactionRepository:

    def __init__(self):
        pass

    def save_transactions(self, transactions: List[Transaction]):
        for transaction_model in map_to_model_list(transactions):
            db.session.add(transaction_model)

        db.session.commit()

    def save(self, transaction: Transaction):
        db.session.add(map_to_model(transaction))
        db.session.commit()

    def delete_by_id(self, transaction_id: int):
        TransactionModel.query.filter(TransactionModel.id == transaction_id).delete()
        db.session.commit()

    def update(self, transaction: Transaction):
        db.session.merge(map_to_model(transaction))
        db.session.commit()

    def get_by_month_year(self, month: int, year: int) -> List[Transaction]:
        transactions = TransactionModel.query.filter(
            extract('month', TransactionModel.date) == month,
            extract('year', TransactionModel.date) == year
        ).order_by(TransactionModel.date.desc()).all()

        return map_to_entity_list(transactions)

    def get_by_id(self, id: int) -> Transaction:
        transaction_model = TransactionModel.query.filter_by(id=id).first()
        return map_to_domain(transaction_model)

    def get_last_uncategorized(self) -> Transaction:
        model = (TransactionModel.query
                 .filter_by(category_id=None)
                 .order_by(TransactionModel.date.desc())
                 .first())
        return map_to_domain(model)

    def get_uncategorized_by_month_year(self, month: int, year: int) -> List[Transaction]:
        transactions = TransactionModel.query.filter(
            extract('month', TransactionModel.date) == month,
            extract('year', TransactionModel.date) == year,
            TransactionModel.category_id.is_(None)
        ).order_by(TransactionModel.date.desc()).all()

        return map_to_entity_list(transactions)

    def find_all(self):
        transactions = TransactionModel.query.all()
        return map_to_entity_list(transactions)