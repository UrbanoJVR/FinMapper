from datetime import datetime
from decimal import Decimal
from typing import List
from unittest import TestCase
from unittest.mock import Mock, call

from app.src.application.transaction.command.categorization.categorize_transactions_command import \
    CategorizedTransaction, CategorizeTransactionsCommand
from app.src.application.transaction.command.categorization.categorize_transactions_command_handler import \
    CategorizeTransactionsCommandHandler
from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from test.unit.domain.transaction.mother.transaction_mother import TransactionMother


class TestCategorizeTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = CategorizeTransactionsCommandHandler(
            transaction_repository=self.mock_transaction_repository,
            category_repository=self.mock_category_repository)
        self.transaction_mother = TransactionMother()

    def test_execute_success(self):
        categorized_transaction_1 = CategorizedTransaction(1, 1)
        categorized_transactions: List[CategorizedTransaction] = [categorized_transaction_1]
        command = CategorizeTransactionsCommand(categorized_transactions)

        category_from_db = Category(
            name="Category name",
            description="Category description",
            id=1
        )
        transaction_from_db = Transaction(
            transaction_date=TransactionDate(datetime.now().date()),
            amount=TransactionAmount(Decimal.from_float(30.10)),
            concept="Concept",
            category=category_from_db,
            id=1)
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db
        self.mock_category_repository.get_by_id.return_value = category_from_db

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_any_call(categorized_transaction_1.transaction_id)
        self.mock_transaction_repository.update.assert_any_call(transaction_from_db)

    def test_execute_multiple(self):
        categorized_transactions = [
            CategorizedTransaction(transaction_id=1, category_id=10),
            CategorizedTransaction(transaction_id=2, category_id=20)
        ]
        command = CategorizeTransactionsCommand(categorized_transactions)

        category_1 = Category(name="Category 1", description="Desc 1", id=10)
        category_2 = Category(name="Category 2", description="Desc 2", id=20)

        transaction_1 = self.transaction_mother.random_with_empty_category()
        transaction_2 = self.transaction_mother.random_with_empty_category()

        self.mock_transaction_repository.get_by_id.side_effect = [transaction_1, transaction_2]
        self.mock_category_repository.get_by_id.side_effect = [category_1, category_2]

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_has_calls([call(categorized_transactions[0].transaction_id), call(categorized_transactions[1].transaction_id)])
        self.mock_category_repository.get_by_id.assert_has_calls([call(categorized_transactions[0].category_id), call(categorized_transactions[1].category_id)])
        self.assertEqual(self.mock_transaction_repository.update.call_count, 2)
        updated_transaction_1 = self.mock_transaction_repository.update.call_args_list[0][0][0]
        updated_transaction_2 = self.mock_transaction_repository.update.call_args_list[1][0][0]
        self.assertEqual(updated_transaction_1.category, category_1)
        self.assertEqual(updated_transaction_2.category, category_2)

