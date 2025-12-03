from datetime import date
from unittest import TestCase
from unittest.mock import Mock
from decimal import Decimal

from app.src.application.report.calculate_monthly_data_for_category_query_handler import \
    CalculateMonthlyDataForCategoryQueryHandler
from app.src.domain.report.month import Month
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from app.src.domain.category import Category


class TestCalculateMonthlyDataForCategoryQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = CalculateMonthlyDataForCategoryQueryHandler(self.mock_transaction_repository)

    def test_execute(self):
        category = Category(id=1, name="Groceries", description="Groceries")
        year = 2024
        transactions_per_month = [
            [Transaction(amount=TransactionAmount(Decimal("-100.00")), concept="Transaction 1", type=TransactionType.EXPENSE, transaction_date=TransactionDate(date(year, 1, 1))),
             Transaction(amount=TransactionAmount(Decimal("-900.50")), concept="Transaction 1", type=TransactionType.EXPENSE, transaction_date=TransactionDate(date(year, 1, 2)))],
            [Transaction(amount=TransactionAmount(Decimal("-200.00")), concept="Transaction 2", type=TransactionType.EXPENSE, transaction_date=TransactionDate(date(year, 2, 1)))],
            [],
            [Transaction(amount=TransactionAmount(Decimal("-300.00")), concept="Transaction 3", type=TransactionType.EXPENSE, transaction_date=TransactionDate(date(year, 4, 1)))],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]

        self.mock_transaction_repository.get_by_month_year_and_category_id.side_effect = transactions_per_month

        result = self.sut.execute(category, year)

        self.assertEqual(self.mock_transaction_repository.get_by_month_year_and_category_id.call_count, 12)

        for month in Month:
            self.mock_transaction_repository.get_by_month_year_and_category_id.assert_any_call(month.value, year,
                                                                                               category.id)

        expected_total_amounts_and_cumulative_averages = [
            (Decimal("-1000.50"), Decimal("-1000.50")),
            (Decimal("-200.00"), Decimal("-600.25")),
            (Decimal("0.00"), Decimal("-400.17")),
            (Decimal("-300.00"), Decimal("-375.12")),
            (Decimal("0.00"), Decimal("-300.10")),
            (Decimal("0.00"), Decimal("-250.08")),
            (Decimal("0.00"), Decimal("-214.36")),
            (Decimal("0.00"), Decimal("-187.56")),
            (Decimal("0.00"), Decimal("-166.72")),
            (Decimal("0.00"), Decimal("-150.05")),
            (Decimal("0.00"), Decimal("-136.41")),
            (Decimal("0.00"), Decimal("-125.04"))
        ]

        for month, (expected_amount, expected_average) in zip(Month, expected_total_amounts_and_cumulative_averages):
            self.assertEqual(result[month].total_amount, expected_amount)
            self.assertEqual(result[month].cumulative_average, expected_average)
