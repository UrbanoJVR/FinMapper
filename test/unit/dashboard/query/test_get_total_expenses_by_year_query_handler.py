from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.dashboard.query.get_total_expenses_by_year_query_handler import \
    GetTotalExpensesByYearQuery, GetTotalExpensesByYearQueryHandler
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetTotalExpensesByYearQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetTotalExpensesByYearQueryHandler(self.mock_transaction_repository)

    def test_given_transactions_for_year_then_return_sum_of_amounts(self):
        transaction1 = Transaction(transaction_date=None, amount=Decimal("100.50"), concept="Test 1")
        transaction2 = Transaction(transaction_date=None, amount=Decimal("200.25"), concept="Test 2")
        transaction3 = Transaction(transaction_date=None, amount=Decimal("50.00"), concept="Test 3")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2, transaction3]

        result = self.sut.execute(GetTotalExpensesByYearQuery(2024))

        assert result == Decimal("350.75")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_no_transactions_for_year_then_return_zero(self):
        self.mock_transaction_repository.get_by_year.return_value = []

        result = self.sut.execute(GetTotalExpensesByYearQuery(2024))

        assert result == Decimal("0.00")
        self.mock_transaction_repository.get_by_year.assert_called_once_with(2024)

    def test_given_negative_amounts_then_return_correct_sum(self):
        transaction1 = Transaction(transaction_date=None, amount=Decimal("-100.00"), concept="Expense 1")
        transaction2 = Transaction(transaction_date=None, amount=Decimal("-50.50"), concept="Expense 2")
        
        self.mock_transaction_repository.get_by_year.return_value = [transaction1, transaction2]

        result = self.sut.execute(GetTotalExpensesByYearQuery(2024))

        assert result == Decimal("-150.50")
