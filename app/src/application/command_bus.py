from app.src.application.transaction.command.categorization.categorize_transactions_command import \
    CategorizeTransactionsCommand
from app.src.application.transaction.command.categorization.categorize_transactions_command_handler import \
    CategorizeTransactionsCommandHandler
from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.application.transaction.command.create_transaction_command_handler import CreateTransactionCommandHandler
from app.src.application.transaction.command.delete_transaction_command_handler import DeleteTransactionCommandHandler, \
    DeleteTransactionCommand
from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand
from app.src.application.transaction.command.update_transaction_command_handler import UpdateTransactionCommandHandler
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

        if isinstance(command, CategorizeTransactionsCommand):
            handler = CategorizeTransactionsCommandHandler(self.transaction_repository, self.category_repository)
            handler.execute(command)

        if isinstance(command, UpdateTransactionCommand):
            handler = UpdateTransactionCommandHandler(self.transaction_repository, self.category_repository)
            handler.execute(command)

        if isinstance(command, DeleteTransactionCommand):
            handler = DeleteTransactionCommandHandler(self.transaction_repository)
            handler.execute(command)