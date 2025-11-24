from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_dashboard_summary_query_handler import (
    GetDashboardSummaryQuery, GetDashboardSummaryQueryHandler, DashboardSummaryResult
)
from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetDashboardSummaryQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetDashboardSummaryQueryHandler(self.mock_transaction_repository)

    def test_given_no_transactions_then_return_zero_values(self):
        self.mock_transaction_repository.get_by_year.return_value = []

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        expected = DashboardSummaryResult(
            year=2024,
            total_expense_amount=Decimal("0.00"),
            average_expense_amount=Decimal("0.00"),
            total_transactions_count=0,
            months_with_data=set()
        )
        assert result == expected
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_then_calculate_correct_total_expense_amount(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.50"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 6, 20), amount=Decimal("200.25"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 12, 10), amount=Decimal("50.00"), concept="Test 3")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.total_expense_amount == Decimal("350.75")
        assert result.year == 2024
        assert result.months_with_data == {1, 6, 12}
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_transactions_in_multiple_months_then_calculate_correct_average(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("300.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 2, 10), amount=Decimal("300.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 3, 20), amount=Decimal("300.00"), concept="Test 3")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.average_expense_amount == Decimal("300.00")
        assert result.total_expense_amount == Decimal("900.00")
        assert result.months_with_data == {1, 2, 3}

    def test_given_transactions_in_single_month_then_average_equals_total(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("200.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 1, 25), amount=Decimal("150.00"), concept="Test 3")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.average_expense_amount == Decimal("450.00")
        assert result.total_expense_amount == Decimal("450.00")
        assert result.months_with_data == {1}

    def test_given_mixed_positive_negative_amounts_then_calculate_correct_total(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("200.00"), concept="Income")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("-50.00"), concept="Expense")
        transaction3 = Transaction(transaction_date=date(2024, 6, 10), amount=Decimal("-100.00"), concept="Expense")
        transaction4 = Transaction(transaction_date=date(2024, 6, 15), amount=Decimal("150.00"), concept="Income")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3,
                                                                     transaction4]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.total_expense_amount == Decimal("200.00")
        assert result.months_with_data == {1, 6}

    def test_given_mixed_amounts_in_two_months_then_calculate_correct_average(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("200.00"), concept="Income")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("-50.00"), concept="Expense")
        transaction3 = Transaction(transaction_date=date(2024, 6, 10), amount=Decimal("-100.00"), concept="Expense")
        transaction4 = Transaction(transaction_date=date(2024, 6, 15), amount=Decimal("150.00"), concept="Income")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3,
                                                                     transaction4]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.average_expense_amount == Decimal("100.00")
        assert result.total_expense_amount == Decimal("200.00")
        assert result.months_with_data == {1, 6}

    def test_given_no_transactions_then_return_zero_transactions_count(self):
        self.mock_transaction_repository.get_by_year.return_value = []

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.total_transactions_count == 0
        assert result.months_with_data == set()

    def test_given_transactions_then_return_correct_transactions_count(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Test 1")
        transaction2 = Transaction(transaction_date=date(2024, 2, 10), amount=Decimal("200.00"), concept="Test 2")
        transaction3 = Transaction(transaction_date=date(2024, 6, 20), amount=Decimal("300.00"), concept="Test 3")
        transaction4 = Transaction(transaction_date=date(2024, 12, 5), amount=Decimal("400.00"), concept="Test 4")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3,
                                                                     transaction4]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.total_transactions_count == 4
        assert result.months_with_data == {1, 2, 6, 12}

    def test_given_transactions_across_different_months_then_return_all_months_with_data(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Jan")
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("50.00"), concept="Jan2")
        transaction3 = Transaction(transaction_date=date(2024, 3, 10), amount=Decimal("200.00"), concept="Mar")
        transaction4 = Transaction(transaction_date=date(2024, 6, 5), amount=Decimal("150.00"), concept="Jun")
        transaction5 = Transaction(transaction_date=date(2024, 12, 25), amount=Decimal("300.00"), concept="Dec")

        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3,
                                                                     transaction4, transaction5]

        result = self.sut.execute(GetDashboardSummaryQuery(2024))

        assert result.months_with_data == {1, 3, 6, 12}
        assert 2 not in result.months_with_data
