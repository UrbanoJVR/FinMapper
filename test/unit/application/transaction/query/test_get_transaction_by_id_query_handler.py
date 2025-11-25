from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQueryHandler
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestGetTransactionByIdQueryHandler(TestCase):

    def setUp(self):
        self.mock_transaction_repository = Mock(spec=TransactionRepository)
        self.sut = GetTransactionByIdQueryHandler(self.mock_transaction_repository)

    def test_execute(self):
        expected_transaction = Transaction(id=1, amount=Decimal(200), concept="concept",
                                           transaction_date=TransactionDate(datetime.now().date()),
                                           category=None)
        result = self.mock_transaction_repository.get_by_id.return_value = expected_transaction

        assert expected_transaction == result
