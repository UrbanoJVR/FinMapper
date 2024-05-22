from typing import List

from sqlalchemy import extract

from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_model_mapper import map_to_model_list, \
    map_to_entity_list, map_to_entity, map_to_model
from app.src.transactions.model.transaction_model import TransactionModel
from database import db


class TransactionRepository:

    def __init__(self):
        pass

    def save_transactions(self, transactions: List[Transaction]):
        for tm in map_to_model_list(transactions):
            db.session.add(tm)

        db.session.commit()

    def save(self, transaction: Transaction):
        db.session.add(map_to_model(transaction))
        db.session.commit()

    def delete(self, transaction_id: int):
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

        # transactions = TransactionModel.query.all()

        return map_to_entity_list(transactions)

    def get_by_id(self, id: int) -> Transaction:
        transaction_model = TransactionModel.query.filter_by(id=id).first()
        return map_to_entity(transaction_model)
