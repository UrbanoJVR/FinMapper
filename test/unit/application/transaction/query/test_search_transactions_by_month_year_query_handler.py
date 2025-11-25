from datetime import date
from decimal import Decimal
from typing import List
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.application.transaction.query.search_transactions_by_month_year_query_handler import \
    SearchTransactionsByMonthYearQueryHandler
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestSearchTransactionsByMonthYearQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = SearchTransactionsByMonthYearQueryHandler(self.mock_transaction_repository)

    def test_execute(self):
        expected_list: List[Transaction] = [
            Transaction(id=1, concept="concept", amount=Decimal(19), category=None, transaction_date=TransactionDate(date.today()))]
        self.mock_transaction_repository.get_by_month_year.return_value = expected_list
        query = SearchTransactionsByMonthYearQuery(month=10, year=2024)

        result = self.sut.execute(query)

        assert result == expected_list
