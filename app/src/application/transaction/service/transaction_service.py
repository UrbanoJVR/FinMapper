from typing import List

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TransactionService:
    repository: TransactionRepository

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def save_transactions(self, transactions: List[Transaction]):
        self.repository.save_transactions(transactions)

    def update(self, transaction: Transaction):
        transaction_from_db = self.repository.get_by_id(transaction.id)
        if transaction_from_db is None:
            # Exception
            return None

        self.repository.update(transaction)

        return transaction.id

    def create(self, transaction: Transaction):
        self.repository.save(transaction)

    def delete(self, id: int):
        self.repository.delete(id)

    def get_by_month_year(self, month: int, year: int) -> List[Transaction]:
        return self.repository.get_by_month_year(month, year)

    def get_by_id(self, id: int) -> Transaction:
        return self.repository.get_by_id(id)
