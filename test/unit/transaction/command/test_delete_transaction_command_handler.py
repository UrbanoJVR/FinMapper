from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.command.delete_transaction_command_handler import DeleteTransactionCommandHandler, \
    DeleteTransactionCommand
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestDeleteTransactionCommandHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = DeleteTransactionCommandHandler(self.mock_transaction_repository)

    def test_execute(self):
        self.sut.execute(DeleteTransactionCommand(1))

        self.mock_transaction_repository.delete_by_id.assert_called_once_with(1)