from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CreateTransactionCommandHandler:

    def __init__(self, transaction_repository: TransactionRepository, category_repository: CategoryRepository):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def execute(self, command: CreateTransactionCommand):
        category = None

        if command.category_id is not None:
            category = self.category_repository.get_by_id(command.category_id)

        transaction = Transaction(
            concept=command.concept,
            amount=command.amount,
            transaction_date=command.date,
            category=category,
            id=None
        )

        self.transaction_repository.save(transaction)
