from typing import List

from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository


class TransactionService:
    repository: TransactionRepository

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def save_transactions(self, transactions: List[Transaction]):
        self.repository.save_transactions(transactions)

    def get_by_month_year(self, month: int, year: int) -> List[Transaction]:
        return self.repository.get_by_month_year(month, year)