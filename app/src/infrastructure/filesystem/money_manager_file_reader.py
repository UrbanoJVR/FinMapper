import logging
import re
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_EVEN
from io import BytesIO

import pyexcel as pe

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.filesystem.transactions_file_reader import TransactionsFileReader
from app.src.infrastructure.repository.category_repository import CategoryRepository


class MoneyManagerFileReader(TransactionsFileReader):
    DATE_HEADER = "Fecha"
    CONCEPT_HEADER = "Nota"
    COMMENTS_HEADER = "Descripción"
    AMOUNT_HEADER = "EUR"
    CATEGORY_HEADER = "Categoría"
    TRANSACTION_TYPE_HEADER = "Ingreso/Gasto"

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def read_all_transactions(self, file: BytesIO) -> list[Transaction]:
        transactions = []

        sheet = pe.get_sheet(file_type='xls', file_content=file.read())
        sheet.name_columns_by_row(0)  # usa la primera fila como cabecera
        records = [dict(zip(sheet.colnames, row)) for row in sheet.rows()]

        for i, row in enumerate(records):
            if not isinstance(row, dict):
                logging.warning("Fila %d no es un diccionario: %s", i, row)
                continue

            try:
                transaction = Transaction(
                    transaction_date=TransactionDate(self._parse_date(row.get(self.DATE_HEADER))),
                    concept=self._parse_concept(row.get(self.CONCEPT_HEADER)),
                    comments=str(row.get(self.COMMENTS_HEADER, "")),
                    amount=self._parse_amount(row.get(self.AMOUNT_HEADER), row.get(self.TRANSACTION_TYPE_HEADER)),
                    category=self._find_category_by_name(row.get(self.CATEGORY_HEADER))
                )
                transactions.append(transaction)
            except Exception as e:
                logging.warning("Error parsing row %d: %s", i, e)

        return transactions

    def _find_category_by_name(self, category_name: str) -> Category | None:
        if not category_name or str(category_name).strip() == "":
            return None

        clean_name = re.sub(r'[^\w\s]', '', str(category_name)).strip()
        return self.category_repository.get_by_name(clean_name)

    def _parse_date(self, cell_value) -> date:
        if not cell_value or str(cell_value).strip() == "":
            logging.exception("Date cannot be empty")
            raise ValueError("Date cannot be empty")

        value = str(cell_value).strip()

        formats = [
            "%d/%m/%Y %H:%M:%S",  # Ej: 30/06/2025 22:50:02
            "%d/%m/%Y",  # Ej: 01/06/2025
            "%Y-%m-%d",  # ISO por si acaso
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue

        logging.exception("Invalid date format: %s", value)
        raise ValueError(f"Invalid date format: {value}")

    def _parse_concept(self, cell_value) -> str:
        if not cell_value or str(cell_value).strip() == "":
            logging.exception("Concept cannot be empty")
            raise ValueError("Concept cannot be empty")

        return str(cell_value).strip()

    def _parse_amount(self, cell_value, type_value: str) -> Decimal:
        if not cell_value or str(cell_value).strip() == "":
            logging.exception("Amount cannot be empty")
            raise ValueError("Amount cannot be empty")

        sign = -1 if str(type_value).strip().upper() == "GASTO" else 1
        return sign * Decimal(str(cell_value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
