from datetime import datetime, date
from decimal import Decimal

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestTransactionRepositoryIT:

    def setup_method(self):
        self.sut = TransactionRepository()

    def test_save_and_find_all(self, test_db):
        transaction = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                  category=None, concept="Concept")
        self.sut.save(transaction)

        transactions = self.sut.find_all()

        assert len(transactions) == 1
        assert transactions[0].id == transaction.id
        assert transactions[0].amount == transaction.amount
