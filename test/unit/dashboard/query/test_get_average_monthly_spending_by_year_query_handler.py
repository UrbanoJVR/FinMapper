from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_average_monthly_spending_by_year_query_handler import \
    GetAverageMonthlySpendingByYearQuery, GetAverageMonthlySpendingByYearQueryHandler
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetAverageMonthlySpendingByYearQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetAverageMonthlySpendingByYearQueryHandler(self.mock_transaction_repository)

    def test_given_transactions_in_three_distinct_months_then_return_average(self):
        # Arrange: 3 months (Jan, Feb, Mar) with total 900
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("300.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 2, 10), amount=Decimal("300.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 3, 20), amount=Decimal("300.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        # Act
        result = self.sut.execute(GetAverageMonthlySpendingByYearQuery(2024))

        # Assert: 900 / 3 = 300
        assert result == Decimal("300.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_no_transactions_then_return_zero(self):
        # Arrange
        self.mock_transaction_repository.get_by_year.return_value = []

        # Act
        result = self.sut.execute(GetAverageMonthlySpendingByYearQuery(2024))

        # Assert
        assert result == Decimal("0.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_in_single_month_then_return_total(self):
        # Arrange: All transactions in January
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("200.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 1, 25), amount=Decimal("150.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        # Act
        result = self.sut.execute(GetAverageMonthlySpendingByYearQuery(2024))

        # Assert: 450 / 1 = 450
        assert result == Decimal("450.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_in_two_months_with_mixed_amounts_then_return_correct_average(self):
        # Arrange: 2 months with mixed positive and negative amounts
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("200.00"), concept="Income")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("-50.00"), concept="Expense")
        transaction3 = Transaction(transaction_date=date(2024, 6, 10), amount=Decimal("-100.00"), concept="Expense")
        transaction4 = Transaction(transaction_date=date(2024, 6, 15), amount=Decimal("150.00"), concept="Income")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3, transaction4]

        # Act
        result = self.sut.execute(GetAverageMonthlySpendingByYearQuery(2024))

        # Assert: (200 - 50 - 100 + 150) / 2 = 200 / 2 = 100
        assert result == Decimal("100.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_multiple_transactions_same_month_then_count_month_once(self):
        # Arrange: Multiple transactions in the same month
        transaction1 = Transaction(transaction_date=date(2024, 3, 1), amount=Decimal("100.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 3, 10), amount=Decimal("100.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 3, 20), amount=Decimal("100.00"), concept="Test 3")
        transaction4 = Transaction(transaction_date=date(2024, 3, 30), amount=Decimal("100.00"), concept="Test 4")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3, transaction4]

        # Act
        result = self.sut.execute(GetAverageMonthlySpendingByYearQuery(2024))

        # Assert: 400 / 1 = 400 (not 400 / 4)
        assert result == Decimal("400.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

