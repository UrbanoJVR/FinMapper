from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQueryHandler
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from test.unit.domain.transaction.mother.transaction_mother import TransactionMother


class TestGetTransactionByIdQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetTransactionByIdQueryHandler(self.mock_transaction_repository)
        self.transaction_mother = TransactionMother()

    def test_execute(self):
        expected_transaction = self.transaction_mother.random_expense_with_empty_category()
        result = self.mock_transaction_repository.get_by_id.return_value = expected_transaction

        assert expected_transaction == result
