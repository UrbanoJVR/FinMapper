from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class DeleteTransactionCommandHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, transaction_id: int):
        self.transaction_repository.delete_by_id(transaction_id)