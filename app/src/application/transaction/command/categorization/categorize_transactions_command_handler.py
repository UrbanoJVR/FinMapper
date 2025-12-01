from app.src.application.transaction.command.categorization.categorize_transactions_command import \
    CategorizeTransactionsCommand
from app.src.infrastructure.repository.category_repository import CategoryRepository

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CategorizeTransactionsCommandHandler:

    def __init__(self,
                 transaction_repository: TransactionRepository,
                 category_repository: CategoryRepository):
        self.transactionRepository = transaction_repository
        self.categoryRepository = category_repository

    def execute(self, command: CategorizeTransactionsCommand):
        for categorized_transaction in command.categorized_transactions:
            transaction_from_db = self.transactionRepository.get_by_id(categorized_transaction.transaction_id)
            updated_transaction = transaction_from_db.change_category(self.categoryRepository.get_by_id(categorized_transaction.category_id))
            self.transactionRepository.update(updated_transaction)

