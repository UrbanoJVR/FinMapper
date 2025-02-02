import logging
import re
from datetime import date
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

        data_frame = pd.read_excel(file, engine="openpyxl")

        for _, row in data_frame.iterrows():
            transaction = Transaction(
                transaction_date=self._parse_date(row[self.DATE_HEADER]),
                concept=self._parse_concept(row[self.CONCEPT_HEADER]),
                comments=str(row[self.COMMENTS_HEADER]),
                amount=self._parse_amount(row[self.AMOUNT_HEADER]),
                category=self._find_category_by_name(row[self.CATEGORY_HEADER])
            )
            transactions.append(transaction)

        return transactions

    def _find_category_by_name(self, category_name: str) -> Category | None:
        if pd.isna(category_name) or category_name.strip() == "":
            return None

        # delete emojis and spaces from name
        clean_name = re.sub(r'[^\w\s]', '', category_name).strip()

        return self.category_repository.get_by_name(clean_name)

    def _parse_date(self, row_value: str) -> date:
        if pd.isna(row_value) or str(row_value).strip() == "":
            logging.exception("Date cannot be empty")
            raise ValueError("Date cannot be empty")

        return pd.to_datetime(row_value, dayfirst=True, errors="raise").date()

    def _parse_concept(self, row_value: str) -> str:
        if pd.isna(row_value) or str(row_value).strip() == "":
            logging.exception("Concept cannot be empty")
            raise ValueError("Concept cannot be empty")

        return row_value

    def _parse_amount(self, row_value: str) -> Decimal:
        if pd.isna(row_value) or str(row_value).strip() == "":
            logging.exception("Amount cannot be empty")
            raise ValueError("Amount cannot be empty")

        return Decimal(row_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
