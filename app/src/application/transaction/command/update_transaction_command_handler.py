from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class UpdateTransactionCommandHandler:

    def __init__(self, transaction_repository: TransactionRepository, category_repository: CategoryRepository):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def execute(self, command: UpdateTransactionCommand):
        transaction = self.transaction_repository.get_by_id(command.transaction_id)
        if transaction is None:
            return

        transaction = self._update_transaction_from_command(transaction, command)

        self.transaction_repository.update(transaction)

    def _update_transaction_from_command(self, transaction: Transaction, command: UpdateTransactionCommand) -> Transaction:
        category = None
        if command.category_id is not None:
            category = self.category_repository.get_by_id(command.category_id)
        
        return transaction.update(
            TransactionDate(command.date),
            TransactionAmount(command.amount),
            command.concept,
            command.type,
            command.comments,
            category
        )
