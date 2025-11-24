from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CreateMultipleTransactionsCommandHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, transactions: list[Transaction]):
        self.transaction_repository.save_transactions(transactions)
