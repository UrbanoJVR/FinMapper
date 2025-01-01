from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class GetTransactionByIdQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, transaction_id: int):
        return self.transaction_repository.get_by_id(transaction_id)
