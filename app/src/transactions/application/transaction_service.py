from typing import List

from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.domain.transaction_from_file import TransactionFromFile
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository


class TransactionService:
    repository: TransactionRepository

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def save_transactions(self, transactions: List[Transaction]):
        self.repository.save_transactions(transactions)
