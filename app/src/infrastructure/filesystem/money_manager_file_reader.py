from io import BytesIO

from app.src.domain.transaction import Transaction
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader


class MoneyManagerFileReader(TransactionsFileReader):

    @staticmethod
    def read_all_transactions(file: BytesIO) -> list[Transaction]:
        transactions = []

        return transactions