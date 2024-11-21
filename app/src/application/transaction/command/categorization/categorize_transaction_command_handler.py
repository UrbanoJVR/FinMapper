from typing import List

from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.application.transaction.command.categorization.categorize_transaction_command import CategorizedTransaction

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CategorizeTransactionCommandHandler:

    def __init__(self,
                 transaction_repository: TransactionRepository,
                 category_repository: CategoryRepository):
        self.transactionRepository = transaction_repository
        self.categoryRepository = category_repository

    def execute(self, categorized_transactions: List[CategorizedTransaction]):
        for categorized_transaction in categorized_transactions:
            transaction_from_db = self.transactionRepository.get_by_id(categorized_transaction.transaction_id)
            transaction_from_db.category = self.categoryRepository.get_by_id(categorized_transaction.category_id)
            self.transactionRepository.update(transaction_from_db)

