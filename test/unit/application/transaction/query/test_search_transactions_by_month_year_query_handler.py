from typing import List
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.application.transaction.query.search_transactions_by_month_year_query_handler import \
    SearchTransactionsByMonthYearQueryHandler
from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from test.unit.domain.transaction.mother.transaction_mother import TransactionMother


class TestSearchTransactionsByMonthYearQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = SearchTransactionsByMonthYearQueryHandler(self.mock_transaction_repository)
        self.transaction_mother = TransactionMother()

    def test_execute(self):
        expected_list: List[Transaction] = [
            self.transaction_mother.random_with_empty_category()]
        self.mock_transaction_repository.get_by_month_year.return_value = expected_list
        query = SearchTransactionsByMonthYearQuery(month=10, year=2024)

        result = self.sut.execute(query)

        assert result == expected_list
