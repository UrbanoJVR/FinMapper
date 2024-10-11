from typing import List

from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.transactions.application.categorization.categorize_transaction_command import CategorizedTransaction

from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository


class CategorizeTransactionCommandHandler:

    def __init__(self,
                 categorized_transactions: List[CategorizedTransaction],
                 transaction_repository: TransactionRepository,
                 category_repository: CategoryRepository):
        self.categorized_transactions = categorized_transactions
        self.transactionRepository = transaction_repository
        self.categoryRepository = category_repository

    def execute(self):
        for categorized_transaction in self.categorized_transactions:
            transaction_from_db = self.transactionRepository.get_by_id(categorized_transaction.transaction_id)
            transaction_from_db.category = self.categoryRepository.get_by_id(categorized_transaction.category_id)
            self.transactionRepository.update(transaction_from_db)
