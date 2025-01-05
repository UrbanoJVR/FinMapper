from app.src.domain.transaction import Transaction
from app.src.infrastructure.in_memory.transaction_memory_repository import TransactionMemoryRepository


class GetTransactionsInMemoryQueryHandler:

    def __init__(self, transaction_memory_repository: TransactionMemoryRepository):
        self.transaction_repository = transaction_memory_repository

    def execute(self) -> list[Transaction]:
        return self.transaction_repository.get_transactions()