from typing import List

from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.application.transaction.command.categorization.categorize_transaction_command import CategorizedTransaction

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CategorizeTransactionCommandHandler:

    # TODO siguiente paso para mejorar command es contenedor de dependencias para poder inyectar en lugar de pasar por constructor

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
