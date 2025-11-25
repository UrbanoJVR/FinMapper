from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand
from app.src.application.transaction.command.update_transaction_command_handler import UpdateTransactionCommandHandler
from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestUpdateTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = UpdateTransactionCommandHandler(self.mock_transaction_repository, self.mock_category_repository)

    def test_execute_success(self):
        command = UpdateTransactionCommand(
            concept="New concept",
            comments="New comments",
            amount=Decimal(11),
            date=date.today(),
            transaction_id=1,
            category_id=1
        )
        category = self._random_category()
        transaction_from_db = self._random_transaction_with_empty_category()
        expected_transaction_to_update = Transaction(
            amount=command.amount,
            concept=command.concept,
            comments=command.comments,
            category=category,
            transaction_date=command.date,
            id=command.transaction_id
        )
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db
        self.mock_category_repository.get_by_id.return_value = category

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_called_with(command.transaction_id)
        self.mock_category_repository.get_by_id.assert_called_with(command.category_id)
        self.mock_transaction_repository.update.assert_called_with(expected_transaction_to_update)

    def test_should_delete_category_from_transaction(self):
        command = self._command_with_empty_category()
        transaction_from_db_with_category = self._random_transaction()
        expected_transaction_to_update = Transaction(
            amount=command.amount,
            concept=command.concept,
            comments=command.comments,
            category=None,
            transaction_date=command.date,
            id=command.transaction_id
        )
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db_with_category

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_called_with(command.transaction_id)
        self.mock_transaction_repository.update.assert_called_with(expected_transaction_to_update)
        self.mock_category_repository.get_by_id.assert_not_called()

    def test_no_execute_when_transaction_not_found(self):
        command = self._command_with_empty_category()
        self.mock_transaction_repository.get_by_id.return_value = None

        self.sut.execute(command)

        self.mock_transaction_repository.update.assert_not_called()

    @staticmethod
    def _random_category() -> Category:
        return Category(
            description="Category description",
            name="Category name",
            id=1
        )

    @staticmethod
    def _random_transaction_with_empty_category() -> Transaction:
        return Transaction(
            amount=Decimal(10),
            concept="Concept",
            comments="Comments",
            category=None,
            transaction_date=date.today(),
            id=1
        )

    def _random_transaction(self) -> Transaction:
        return Transaction(
            amount=Decimal(10),
            concept="Concept",
            comments="Comments",
            category=self._random_category(),
            transaction_date=date.today(),
            id=1)

    @staticmethod
    def _command_with_empty_category() -> UpdateTransactionCommand:
        return UpdateTransactionCommand(
            concept="New concept",
            comments="New comments",
            amount=Decimal(10),
            date=date.today(),
            transaction_id=1,
            category_id=None
        )
