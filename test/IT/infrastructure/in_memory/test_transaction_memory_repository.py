from datetime import datetime
from decimal import Decimal

import pytest
from flask import Flask

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.in_memory.transaction_memory_repository import TransactionMemoryRepository


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.secret_key = "test_secret_key"
    return app


@pytest.fixture
def flask_request_context(flask_app):
    with flask_app.test_request_context():
        yield


class TestTransactionMemoryRepository:

    def setup_method(self):
        self.sut = TransactionMemoryRepository()

    def test_save_and_get_transactions(self, flask_request_context):
        TransactionMemoryRepository.clear()
        
        transaction1 = Transaction(id=None, category=None, amount=TransactionAmount(Decimal("100.25")), concept="Concept 1",
                                   comments="Comments 1", transaction_date=TransactionDate(datetime.now().date()))
        transaction2 = Transaction(id=None, category=None, amount=TransactionAmount(Decimal("200.99")), concept="Concept 2",
                                   comments="Comments 2", transaction_date=TransactionDate(datetime.now().date()))
        transactions = [transaction1, transaction2]

        TransactionMemoryRepository.save_transactions(transactions)

        result = TransactionMemoryRepository.get_transactions()

        assert len(result) == 2
        
        result_concepts = {t.concept for t in result}
        assert result_concepts == {"Concept 1", "Concept 2"}
        
        result_amounts = {t.amount.value for t in result}
        assert result_amounts == {Decimal("100.25"), Decimal("200.99")}
        
        for transaction in result:
            if transaction.concept == "Concept 1":
                assert transaction.amount.value == Decimal("100.25")
                assert transaction.comments == "Comments 1"
            elif transaction.concept == "Concept 2":
                assert transaction.amount.value == Decimal("200.99")
                assert transaction.comments == "Comments 2"
