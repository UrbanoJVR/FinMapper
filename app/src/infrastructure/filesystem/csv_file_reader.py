from decimal import Decimal
from io import BytesIO

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader
from app.src.shared.date_utils import str_to_date


class CsvFileReader(TransactionsFileReader):

    @staticmethod
    def read_all_transactions(file: BytesIO) -> list[Transaction]:
        transactions = []

        for i, line in enumerate(file):
            line = line.decode('utf-8').strip()

            if i == 0 and line.startswith('\ufeff'):
                line = line[1:]

            if not line:
                continue

            fields = line.split(';')
            transaction = Transaction(
                transaction_date=TransactionDate(str_to_date(fields[0])),
                concept=fields[1],
                amount=Decimal(fields[2].replace(',', '.'))
            )
            transactions.append(transaction)

        return transactions
