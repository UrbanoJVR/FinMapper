from typing import List

from app.src.categories.domain.category import Category
from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.categories.application import category_service


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

    def get_last_month_uncategorized(self) -> List[Transaction]:
        last_uncategorized_transaction = self.repository.get_last_uncategorized()

        if last_uncategorized_transaction is None:
            return []

        return self.repository.get_uncategorized_by_month_year(
            last_uncategorized_transaction.transaction_date.month,
            last_uncategorized_transaction.transaction_date.year)
