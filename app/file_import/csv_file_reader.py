import os
from pathlib import Path

from flask import current_app

from app.file_import.domain.transaction_from_file import TransactionFromFile
from app.file_import.transactions_file_reader import TransactionsFileReader


class CsvFileReader(TransactionsFileReader):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_all_transactions(self):
        path = Path(str(os.path.join(current_app.config['UPLOAD_DIR'], self.file_name)))
        content_lines = path.read_text(encoding='utf-8').strip().splitlines()
        transactions = []

        for line in content_lines[1:]:
            transaction = TransactionFromFile(line.split(';')[0], line.split(';')[1], line.split(';')[2])
            transactions.append(transaction)

        return transactions
