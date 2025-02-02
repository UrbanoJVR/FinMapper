from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.application.transaction.command.create_transaction_command_handler import CreateTransactionCommandHandler
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CommandBus:

    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.category_repository = CategoryRepository()

    def execute(self, command):
        if isinstance(command, CreateTransactionCommand):
            handler = CreateTransactionCommandHandler(self.transaction_repository, self.category_repository)
            handler.execute(command)
