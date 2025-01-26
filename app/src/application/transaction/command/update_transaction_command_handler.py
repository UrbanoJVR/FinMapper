from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand
from app.src.domain.transaction import Transaction
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
        transaction.concept = command.concept
        transaction.comments = command.comments
        transaction.transaction_date = command.date
        transaction.amount = command.amount

        if command.category_id is None:
            transaction.category = None
        else:
            transaction.category = self.category_repository.get_by_id(command.category_id)

        return transaction
