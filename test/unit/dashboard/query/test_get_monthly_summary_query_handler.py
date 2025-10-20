from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_monthly_summary_query_handler import (
    GetMonthlySummaryQuery, GetMonthlySummaryQueryHandler, MonthlySummaryResult
)
from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetMonthlySummaryQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetMonthlySummaryQueryHandler(self.mock_transaction_repository)

    def test_given_no_transactions_then_return_empty_summary(self):
        self.mock_transaction_repository.get_by_month_year.return_value = []

        result = self.sut.execute(GetMonthlySummaryQuery(2024, 1))

        assert result.year == 2024
        assert result.month == 1
        assert result.total_expense_amount == Decimal("0.00")
        assert result.category_expenses == []
        self.mock_transaction_repository.get_by_month_year.assert_called_once_with(1, 2024)

    def test_given_transactions_in_single_category_then_return_correct_summary(self):
        category = Category(id=1, name="Alimentación")
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Mercadona", category=category)
        transaction2 = Transaction(transaction_date=date(2024, 1, 20), amount=Decimal("50.00"), concept="Carrefour", category=category)

        self.mock_transaction_repository.get_by_month_year.return_value = [transaction1, transaction2]

        result = self.sut.execute(GetMonthlySummaryQuery(2024, 1))

        assert result.year == 2024
        assert result.month == 1
        assert result.total_expense_amount == Decimal("150.00")
        assert len(result.category_expenses) == 1
        assert result.category_expenses[0].category_id == 1
        assert result.category_expenses[0].category_name == "Alimentación"
        assert result.category_expenses[0].total_amount == Decimal("150.00")
        assert len(result.category_expenses[0].transactions) == 2

    def test_given_transactions_in_multiple_categories_then_order_by_total_desc(self):
        category1 = Category(id=1, name="Alimentación")
        category2 = Category(id=2, name="Transporte")
        category3 = Category(id=3, name="Vivienda")

        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Mercadona", category=category1)
        transaction2 = Transaction(transaction_date=date(2024, 1, 16), amount=Decimal("300.00"), concept="Alquiler", category=category3)
        transaction3 = Transaction(transaction_date=date(2024, 1, 17), amount=Decimal("50.00"), concept="Gasolina", category=category2)

        self.mock_transaction_repository.get_by_month_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetMonthlySummaryQuery(2024, 1))

        assert len(result.category_expenses) == 3
        assert result.category_expenses[0].category_name == "Vivienda"
        assert result.category_expenses[0].total_amount == Decimal("300.00")
        assert result.category_expenses[1].category_name == "Alimentación"
        assert result.category_expenses[1].total_amount == Decimal("100.00")
        assert result.category_expenses[2].category_name == "Transporte"
        assert result.category_expenses[2].total_amount == Decimal("50.00")

    def test_given_uncategorized_transactions_then_group_as_sin_categoria(self):
        transaction1 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("100.00"), concept="Sin categoría 1", category=None)
        transaction2 = Transaction(transaction_date=date(2024, 1, 16), amount=Decimal("50.00"), concept="Sin categoría 2", category=None)

        self.mock_transaction_repository.get_by_month_year.return_value = [transaction1, transaction2]

        result = self.sut.execute(GetMonthlySummaryQuery(2024, 1))

        assert len(result.category_expenses) == 1
        assert result.category_expenses[0].category_id is None
        assert result.category_expenses[0].category_name == "Sin categoría"
        assert result.category_expenses[0].total_amount == Decimal("150.00")
        assert len(result.category_expenses[0].transactions) == 2

    def test_given_multiple_transactions_per_category_then_sum_correctly(self):
        category = Category(id=1, name="Alimentación")
        transaction1 = Transaction(transaction_date=date(2024, 1, 5), amount=Decimal("25.50"), concept="Test 1", category=category)
        transaction2 = Transaction(transaction_date=date(2024, 1, 10), amount=Decimal("30.25"), concept="Test 2", category=category)
        transaction3 = Transaction(transaction_date=date(2024, 1, 15), amount=Decimal("44.25"), concept="Test 3", category=category)

        self.mock_transaction_repository.get_by_month_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetMonthlySummaryQuery(2024, 1))

        assert result.total_expense_amount == Decimal("100.00")
        assert len(result.category_expenses) == 1
        assert result.category_expenses[0].total_amount == Decimal("100.00")
        assert len(result.category_expenses[0].transactions) == 3
