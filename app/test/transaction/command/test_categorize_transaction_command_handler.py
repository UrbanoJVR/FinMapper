from datetime import datetime
from decimal import Decimal
from typing import List
from unittest import TestCase
from unittest.mock import Mock, MagicMock, call

from app.src.application.transaction.command.categorization.categorized_transaction import CategorizedTransaction
from app.src.application.transaction.command.categorization.categorize_transaction_command_handler import \
    CategorizeTransactionCommandHandler
from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestCategorizeTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = CategorizeTransactionCommandHandler(
            transaction_repository=self.mock_transaction_repository,
            category_repository=self.mock_category_repository)

    def test_execute_success(self):
        categorized_transaction_1 = CategorizedTransaction(1, 1)
        categorized_transactions: List[CategorizedTransaction] = [categorized_transaction_1]

        category_from_db = Category(
            name="Category name",
            description="Category description",
            id=1
        )
        transaction_from_db = Transaction(
            transaction_date=datetime.now(),
            amount=Decimal.from_float(30.10),
            concept="Concept",
            category=category_from_db,
            id=1)
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db
        self.mock_category_repository.get_by_id.return_value = category_from_db

        self.sut.execute(categorized_transactions)

        self.mock_transaction_repository.get_by_id.assert_any_call(categorized_transaction_1.transaction_id)
        self.mock_transaction_repository.update.assert_any_call(transaction_from_db)

    def test_execute_multiple(self):
        categorized_transactions = [
            CategorizedTransaction(transaction_id=1, category_id=10),
            CategorizedTransaction(transaction_id=2, category_id=20)
        ]

        transaction_mock_1 = MagicMock()
        transaction_mock_2 = MagicMock()
        category_mock_1 = MagicMock()
        category_mock_2 = MagicMock()

        self.mock_transaction_repository.get_by_id.side_effect = [transaction_mock_1, transaction_mock_2]
        self.mock_category_repository.get_by_id.side_effect = [category_mock_1, category_mock_2]

        self.sut.execute(categorized_transactions)

        self.mock_transaction_repository.get_by_id.assert_has_calls([call(categorized_transactions[0].transaction_id), call(categorized_transactions[1].transaction_id)])
        self.mock_category_repository.get_by_id.assert_has_calls([call(categorized_transactions[0].category_id), call(categorized_transactions[1].category_id)])
        self.mock_transaction_repository.update.assert_has_calls([call(transaction_mock_1), call(transaction_mock_2)])

