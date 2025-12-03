from datetime import date
from decimal import Decimal, InvalidOperation
from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock

import pyexcel as pe

from app.src.domain.category import Category
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType
from app.src.infrastructure.filesystem.money_manager_file_reader import MoneyManagerFileReader
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestMoneyManagerFileReader(TestCase):

    def setUp(self):
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.reader = MoneyManagerFileReader(self.mock_category_repository)

    def _create_xls_file(self, records: list[dict]) -> BytesIO:
        sheet = pe.get_sheet(records=records)
        output = BytesIO()
        sheet.save_to_memory("xls", output)
        output.seek(0)
        return output

    def test_valid_transaction_with_category(self):
        data = [{
            "Fecha": "01/01/2025 16:20:00",
            "Nota": "Compra Amazon",
            "Descripción": "Pedido #123",
            "EUR": "50.00",
            "Categoría": "🛒 Necesidades básicas",
            "Ingreso/Gasto": "Gasto"
        }]

        self.mock_category_repository.get_by_name.return_value = Category(name="Necesidades básicas", id=1)
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)

        self.assertEqual(len(transactions), 1)
        tx = transactions[0]
        self.assertEqual(tx.concept, "Compra Amazon")
        self.assertEqual(tx.comments, "Pedido #123")
        self.assertEqual(tx.amount, TransactionAmount(Decimal("-50.00")))
        self.assertEqual(tx.category.name, "Necesidades básicas")
        self.assertEqual(tx.transaction_date, TransactionDate(date(2025, 1, 1)))
        self.assertEqual(tx.type, TransactionType.EXPENSE)

    def test_transaction_without_category(self):
        data = [{
            "Fecha": "01/01/2025",
            "Nota": "Pago Netflix",
            "Descripción": "",
            "EUR": "15.00",
            "Categoría": "",
            "Ingreso/Gasto": "Gasto"
        }]

        self.mock_category_repository.get_by_name.return_value = None
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)

        self.assertEqual(len(transactions), 1)
        self.assertIsNone(transactions[0].category)
        self.assertEqual(transactions[0].type, TransactionType.EXPENSE)


    def test_given_invalid_date_then_skip_transaction(self):
        data = [{
            "Fecha": "fecha no válida",
            "Nota": "Compra",
            "Descripción": "",
            "EUR": "10.00",
            "Categoría": "Otros",
            "Ingreso/Gasto": "Gasto"
        }]
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)
        self.assertEqual(len(transactions), 0)

    def test_given_empty_concept_then_skip_transaction(self):
        data = [{
            "Fecha": "01/01/2025",
            "Nota": "",
            "Descripción": "",
            "EUR": "20.00",
            "Categoría": "Otros",
            "Ingreso/Gasto": "Gasto"
        }]
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)
        self.assertEqual(len(transactions), 0)

    def test_given_empty_amount_then_skip_transaction(self):
        data = [{
            "Fecha": "01/01/2025",
            "Nota": "Compra",
            "Descripción": "",
            "EUR": "",
            "Categoría": "Otros",
            "Ingreso/Gasto": "Gasto"
        }]
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)
        self.assertEqual(len(transactions), 0)

    def test_given_invalid_amount_then_skip_transaction(self):
        data = [{
            "Fecha": "01/01/2025",
            "Nota": "Compra",
            "Descripción": "",
            "EUR": "noesnumero",
            "Categoría": "Otros",
            "Ingreso/Gasto": "Gasto"
        }]
        file = self._create_xls_file(data)
        transactions = self.reader.read_all_transactions(file)
        self.assertEqual(len(transactions), 0)
