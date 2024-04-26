from typing import List

from app import db
from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_model_mapper import map_to_model_list


class TransactionRepository:

    def __init__(self):
        pass

    def save_transactions(self, transactions: List[Transaction]):
        for tm in map_to_model_list(transactions):
            db.session.add(tm)

        db.session.commit()
