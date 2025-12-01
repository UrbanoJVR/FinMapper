from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.command.update_transaction_command_handler import UpdateTransactionCommandHandler
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from test.unit.application.transaction.command.mother.update_transaction_command_mother import \
    UpdateTransactionCommandMother
from test.unit.domain.category.category_mother import CategoryMother
from test.unit.domain.transaction.mother.transaction_mother import TransactionMother


class TestUpdateTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = UpdateTransactionCommandHandler(self.mock_transaction_repository, self.mock_category_repository)
        self.update_transaction_command_mother = UpdateTransactionCommandMother()
        self.transaction_mother = TransactionMother()
        self.category_mother = CategoryMother()

    def test_execute_success(self):
        category = self.category_mother.random()
        transaction_from_db = self.transaction_mother.random_with_empty_category()
        command = self.update_transaction_command_mother.random_with_transaction_id_and_category_id(
            transaction_from_db.id, category.id)
        expected_transaction_to_update = Transaction(
            amount=TransactionAmount(command.amount),
            concept=command.concept,
            comments=command.comments,
            category=category,
            transaction_date=TransactionDate(command.date),
            id=command.transaction_id
        )
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db
        self.mock_category_repository.get_by_id.return_value = category

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_called_with(command.transaction_id)
        self.mock_category_repository.get_by_id.assert_called_with(command.category_id)
        self.mock_transaction_repository.update.assert_called_with(expected_transaction_to_update)

    def test_should_delete_category_from_transaction(self):
        command = self.update_transaction_command_mother.random_with_empty_category()
        transaction_from_db_with_category = self.transaction_mother.random_with_id(command.transaction_id)
        expected_transaction_to_update = Transaction(
            amount=TransactionAmount(command.amount),
            concept=command.concept,
            comments=command.comments,
            category=None,
            transaction_date=TransactionDate(command.date),
            id=command.transaction_id
        )
        self.mock_transaction_repository.get_by_id.return_value = transaction_from_db_with_category

        self.sut.execute(command)

        self.mock_transaction_repository.get_by_id.assert_called_with(command.transaction_id)
        self.mock_transaction_repository.update.assert_called_with(expected_transaction_to_update)
        self.mock_category_repository.get_by_id.assert_not_called()

    def test_no_execute_when_transaction_not_found(self):
        command = self.update_transaction_command_mother.random_with_empty_category()
        self.mock_transaction_repository.get_by_id.return_value = None

        self.sut.execute(command)

        self.mock_transaction_repository.update.assert_not_called()
