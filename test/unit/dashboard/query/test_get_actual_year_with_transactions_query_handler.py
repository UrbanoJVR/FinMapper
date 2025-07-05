from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_actual_year_with_transactions_query_handler import \
    GetActualYearWithTransactionsQueryHandler
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetActualYearWithTransactionsQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetActualYearWithTransactionsQueryHandler(self.mock_transaction_repository)

    def test_given_no_years_with_transactions_then_return_empty_response(self):
        years_with_transactions: list[int] = []
        self.mock_transaction_repository.get_years_with_transactions.return_value = years_with_transactions

        result = self.sut.execute()

        assert result.year is None

    def test_given