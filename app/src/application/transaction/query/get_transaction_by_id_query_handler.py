from dataclasses import dataclass

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetTransactionByIdQuery:
    transaction_id: int

class GetTransactionByIdQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: GetTransactionByIdQuery):
        return self.transaction_repository.get_by_id(query.transaction_id)