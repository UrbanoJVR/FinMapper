from unittest import TestCase
from unittest.mock import Mock

from freezegun import freeze_time

from app.src.application.dashboard.query.get_latest_available_transaction_year_handler import \
    GetLatestAvailableTransactionYearHandler
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetLatestAvailableTransactionYearHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetLatestAvailableTransactionYearHandler(self.mock_transaction_repository)

    def test_given_no_years_with_transactions_then_return_empty_response(self):
        self.mock_transaction_repository.get_years_with_transactions.return_value = []

        result = self.sut.execute()

        assert result is None

    @freeze_time("2025-07-05")
    def test_given_transactions_in_current_year_then_return_current_year(self):
        self.mock_transaction_repository.get_years_with_transactions.return_value = [2024, 2025, 2026]

        result = self.sut.execute()

        assert result == 2025

    @freeze_time("2025-07-05")
    def test_given_no_transactions_in_current_year_then_return_latest_year_with_transactions(self):
        self.mock_transaction_repository.get_years_with_transactions.return_value = [2024, 2026]

        result = self.sut.execute()

        assert result == 2026
