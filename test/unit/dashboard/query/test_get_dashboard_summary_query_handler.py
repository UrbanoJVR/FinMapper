from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_dashboard_summary_query_handler import (
    GetDashboardSummaryQuery, GetDashboardSummaryQueryHandler, DashboardSummaryResult
)
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetDashboardSummaryQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetDashboardSummaryQueryHandler(self.mock_transaction_repository)

    def test_given_no_transactions_then_return_zero_values(self):
        # Arrange
        self.mock_transaction_repository.get_by_year.return_value = []

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert
        expected = DashboardSummaryResult(
            year=2024,
            total_expense_amount=Decimal("0.00"),
            average_expense_amount=Decimal("0.00")
        )
        assert result == expected
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_then_calculate_correct_total_expense_amount(self):
        # Arrange
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.50"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 6, 20), amount=Decimal("200.25"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 12, 10), amount=Decimal("50.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert
        assert result.total_expense_amount == Decimal("350.75")
        assert result.year == 2024
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_in_multiple_months_then_calculate_correct_average(self):
        # Arrange: 3 months (Jan, Feb, Mar) with total 900
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("300.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 2, 10), amount=Decimal("300.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 3, 20), amount=Decimal("300.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert: 900 / 3 = 300
        assert result.average_expense_amount == Decimal("300.00")
        assert result.total_expense_amount == Decimal("900.00")

    def test_given_transactions_in_single_month_then_average_equals_total(self):
        # Arrange: All transactions in January
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("200.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 1, 25), amount=Decimal("150.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert: 450 / 1 = 450
        assert result.average_expense_amount == Decimal("450.00")
        assert result.total_expense_amount == Decimal("450.00")

    def test_given_mixed_positive_negative_amounts_then_calculate_correct_total(self):
        # Arrange: Mixed positive and negative amounts
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("200.00"), concept="Income")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("-50.00"), concept="Expense")
        transaction3 = Transaction(transaction_date=date(2024, 6, 10), amount=Decimal("-100.00"), concept="Expense")
        transaction4 = Transaction(transaction_date=date(2024, 6, 15), amount=Decimal("150.00"), concept="Income")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3, transaction4]

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert: 200 - 50 - 100 + 150 = 200
        assert result.total_expense_amount == Decimal("200.00")

    def test_given_mixed_amounts_in_two_months_then_calculate_correct_average(self):
        # Arrange: 2 months with mixed positive and negative amounts
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("200.00"), concept="Income")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("-50.00"), concept="Expense")
        transaction3 = Transaction(transaction_date=date(2024, 6, 10), amount=Decimal("-100.00"), concept="Expense")
        transaction4 = Transaction(transaction_date=date(2024, 6, 15), amount=Decimal("150.00"), concept="Income")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3, transaction4]

        # Act
        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        # Assert: (200 - 50 - 100 + 150) / 2 = 200 / 2 = 100
        assert result.average_expense_amount == Decimal("100.00")
        assert result.total_expense_amount == Decimal("200.00")
