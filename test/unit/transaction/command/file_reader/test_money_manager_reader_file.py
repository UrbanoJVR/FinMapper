from decimal import Decimal, InvalidOperation
from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock

import pandas as pd

from app.src.domain.category import Category
from app.src.infrastructure.filesystem.money_manager_file_reader import MoneyManagerFileReader
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestMoneyManagerFileReader(TestCase):

    def setUp(self):
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.reader = MoneyManagerFileReader(self.mock_category_repository)

    def _create_test_excel(self, data: dict) -> BytesIO:
        df = pd.DataFrame(data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        excel_buffer.seek(0)
        return excel_buffer

    def test_read_all_transactions_category_found(self):
        test_data = {
            "Fecha": ["01/01/2025 16:20:00"],
            "Nota": ["Compra en Amazon"],
            "EUR": ["50.00"],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = Category(name="Necesidades básicas", id=1)

        file = self._create_test_excel(test_data)
        transactions = self.reader.read_all_transactions(file)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].concept, "Compra en Amazon")
        self.assertEqual(transactions[0].amount, Decimal("50.00"))
        self.assertIsNotNone(transactions[0].category)
        self.assertEqual(transactions[0].category.name, "Necesidades básicas")

    def test_read_all_transactions_category_not_found(self):
        test_data = {
            "Fecha": ["01/01/2025"],
            "Nota": ["Compra en Amazon"],
            "EUR": ["50.00"],
            "Categoría": ["Categoría Inexistente"]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        transactions = self.reader.read_all_transactions(file)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].concept, "Compra en Amazon")
        self.assertEqual(transactions[0].amount, Decimal("50.00"))
        self.assertIsNone(transactions[0].category)

    def test_read_all_transactions_invalid_date_should_raise_error(self):
        test_data = {
            "Fecha": ["invalid-date"],
            "Nota": ["Compra en Amazon"],
            "EUR": ["50.00"],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = Category(name="Necesidades básicas", id=1)

        file = self._create_test_excel(test_data)
        with self.assertRaises(ValueError):
            self.reader.read_all_transactions(file)

    def test_read_all_transactions_empty_date_should_raise_error(self):
        test_data = {
            "Fecha": [None],
            "Nota": ["Compra en Amazon"],
            "EUR": ["50.00"],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        with self.assertRaises(ValueError):
            self.reader.read_all_transactions(file)

    def test_read_all_transactions_empty_concept_should_raise_error(self):
        test_data = {
            "Fecha": ["01/01/2025 16:20:00"],
            "Nota": [None],
            "EUR": ["50.00"],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        with self.assertRaises(ValueError):
            self.reader.read_all_transactions(file)

    def test_read_all_transactions_empty_amount_should_raise_error(self):
        test_data = {
            "Fecha": ["01/01/2025 16:20:00"],
            "Nota": ["Concept"],
            "EUR": [None],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        with self.assertRaises(ValueError):
            self.reader.read_all_transactions(file)

    def test_read_all_transactions_invalid_amount_should_raise_error(self):
        test_data = {
            "Fecha": ["01/01/2025 16:20:00"],
            "Nota": ["Concept"],
            "EUR": ["Paco pepe"],
            "Categoría": ["🛒 Necesidades básicas"]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        with self.assertRaises(InvalidOperation):
            self.reader.read_all_transactions(file)

    def test_read_all_transactions_empty_category(self):
        test_data = {
            "Fecha": ["01/01/2025 16:20:00"],
            "Nota": ["Concept"],
            "EUR": ["50.00"],
            "Categoría": [None]
        }

        self.mock_category_repository.get_by_name.return_value = None

        file = self._create_test_excel(test_data)
        transactions = self.reader.read_all_transactions(file)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].concept, "Concept")
        self.assertEqual(transactions[0].amount, Decimal("50.00"))
        self.assertIsNone(transactions[0].category)