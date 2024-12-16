from unittest import TestCase
from unittest.mock import Mock

from app.src.application.category.query.is_category_used_query_handler import IsCategoryUsedQueryHandler
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestIsCategoryUsedQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = IsCategoryUsedQueryHandler(self.mock_transaction_repository)

    def test_return_true(self):
        self.mock_transaction_repository.find_first_by_category_id.return_value = Mock(spec=Transaction)

        result = self.sut.execute(1)

        assert result == True

    def test_return_false(self):
        self.mock_transaction_repository.find_first_by_category_id.return_value = None
        result = self.sut.execute(2)

        assert result == False
        self.mock_transaction_repository.find_first_by_category_id.assert_called_once_with(2)