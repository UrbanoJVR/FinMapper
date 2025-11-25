from datetime import datetime
from decimal import Decimal
from typing import List
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.query.search_last_uncategorized_transactions_query_handler import \
    SearchLastUncategorizedTransactionsQueryHandler
from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestSearchUncategorizedTransactionsFromLastMonthQuery(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = SearchLastUncategorizedTransactionsQueryHandler(self.mock_transaction_repository)


    def test_execute_success(self):
        transaction_1: Transaction = Transaction(
            concept="Concept",
            amount=Decimal(100),
            transaction_date=datetime.now(),
            id=1,
            category=None
        )
        transactions_from_db: List[Transaction] = [transaction_1]
        self.mock_transaction_repository.get_last_uncategorized.return_value = transaction_1
        self.mock_transaction_repository.get_uncategorized_by_month_year.return_value = transactions_from_db

        result: List[Transaction] = self.sut.execute()

        self.assertEqual(len(result), len(transactions_from_db))
        self.assertEqual(result, transactions_from_db)


    def test_return_empty_list_when_there_is_not_uncategorized_transaction(self):
        self.mock_transaction_repository.get_last_uncategorized.return_value = None

        result: List[Transaction] = self.sut.execute()

        self.assertEqual(len(result), 0)
        self.mock_transaction_repository.get_uncategorized_by_month_year.assert_not_called()
