from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.application.transaction.command.create_transaction_command_handler import CreateTransactionCommandHandler
from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestCreateTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = CreateTransactionCommandHandler(self.mock_transaction_repository, self.mock_category_repository)


    def test_execute_success(self):
        command = CreateTransactionCommand(
            amount=Decimal(10),
            concept="concept",
            comments="comments",
            category_id=1,
            date=datetime.now()
        )
        category_from_db = Category(
            name="Category name",
            description="Category description",
            id=command.category_id
        )
        transaction = Transaction(
            amount=command.amount,
            transaction_date=command.date,
            concept=command.concept,
            comments=command.comments,
            category=category_from_db,
            id=None
        )
        self.mock_category_repository.get_by_id.return_value = category_from_db

        self.sut.execute(command)

        self.mock_transaction_repository.save.assert_called_with(transaction)


    def test_execute_when_category_not_exists(self):
        command = CreateTransactionCommand(
            amount=Decimal(10),
            concept="concept",
            comments="comments",
            category_id=1,
            date=datetime.now()
        )
        transaction = Transaction(
            amount=command.amount,
            transaction_date=command.date,
            concept=command.concept,
            comments=command.comments,
            category=None,
            id=None
        )
        self.mock_category_repository.get_by_id.return_value = None

        self.sut.execute(command)

        self.mock_transaction_repository.save.assert_called_with(transaction)


    def test_execute_when_empty_category_id(self):
        command = CreateTransactionCommand(
            amount=Decimal(10),
            concept="concept",
            comments="comments",
            date=datetime.now()
        )
        transaction = Transaction(
            amount=command.amount,
            transaction_date=command.date,
            concept=command.concept,
            comments=command.comments,
            category=None,
            id=None
        )
        self.mock_category_repository.get_by_id.assert_not_called()

        self.sut.execute(command)

        self.mock_transaction_repository.save.assert_called_with(transaction)