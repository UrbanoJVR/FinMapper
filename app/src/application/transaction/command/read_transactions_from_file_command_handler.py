from app.src.application.transaction.command.read_transactions_from_file_command import ReadTransactionsFromFileCommand
from app.src.domain.transaction import Transaction
from app.src.infrastructure.filesystem.file_reader_factory import FileReaderFactory
from app.src.infrastructure.in_memory.transaction_memory_repository import TransactionMemoryRepository


class ReadTransactionsFromFileCommandHandler:

    def __init__(self, transaction_memory_repository: TransactionMemoryRepository, reader_factory: FileReaderFactory):
        self.transaction_repository = transaction_memory_repository
        self.reader_factory = reader_factory

    def execute(self, command: ReadTransactionsFromFileCommand):
        transactions: list[Transaction] = (self.reader_factory.get_reader(command.file_type)
                                           .read_all_transactions(command.file.stream))
        self.transaction_repository.save_transactions(transactions)
