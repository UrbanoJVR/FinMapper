from dataclasses import dataclass

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class DeleteTransactionCommand:
    transaction_id: int

class DeleteTransactionCommandHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, command: DeleteTransactionCommand):
        self.transaction_repository.delete_by_id(command.transaction_id)