from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class IsCategoryUsedQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, category_id) -> bool:
        transaction = self.transaction_repository.find_first_by_category_id(category_id)

        if transaction is None:
            return False

        return True