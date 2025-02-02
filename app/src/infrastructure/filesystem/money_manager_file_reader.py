import re
from decimal import Decimal, ROUND_HALF_EVEN
from io import BytesIO

import pandas as pd

from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader
from app.src.infrastructure.repository.category_repository import CategoryRepository


class MoneyManagerFileReader(TransactionsFileReader):

    DATE_HEADER = "Fecha"
    CONCEPT_HEADER = "Nota"
    COMMENTS_HEADER = "Nota"
    AMOUNT_HEADER = "EUR"
    CATEGORY_HEADER = "Categoría"

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def read_all_transactions(self, file: BytesIO) -> list[Transaction]:
        transactions = []

        # TODO raise error cuando falla (puede hacerse en el controlador más genérico y listo)
        data_frame = pd.read_excel(file, engine="openpyxl")

        for _, row in data_frame.iterrows():
            transaction = Transaction(
                transaction_date = pd.to_datetime(row[self.DATE_HEADER], dayfirst=True, errors="coerce").date(),
                concept=str(row[self.CONCEPT_HEADER]),
                comments=str(row[self.COMMENTS_HEADER]),
                amount=Decimal(row[self.AMOUNT_HEADER]).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN),
                category=self._find_category_by_name(row[self.CATEGORY_HEADER])
            )
            transactions.append(transaction)

        return transactions

    def _find_category_by_name(self, category_name: str) -> Category | None:
        # delete emojis and spaces form name
        clean_name = re.sub(r'[^\w\s]', '', category_name).strip()

        return self.category_repository.get_by_name(clean_name)