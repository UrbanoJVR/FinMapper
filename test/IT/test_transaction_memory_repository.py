from datetime import datetime
from decimal import Decimal

import pytest
from flask import Flask

from app.src.domain.transaction import Transaction
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


# @pytest.mark.skip(
#     reason="deshabilitado hasta conseguir hacer que el almacenamiento en la sessión se comporte igual en los tests que en entorno real")
class TestTransactionMemoryRepository:

    def setup_method(self):
        self.sut = TransactionMemoryRepository()

    def test_save_and_get_transactions(self, flask_request_context):
        transactions = [
            Transaction(id=None, category=None, amount=Decimal(100.25), concept="Concept 1",
                        transaction_date=datetime.now()),
            Transaction(id=None, category=None, amount=Decimal(200.99), concept="Concept 2",
                        transaction_date=datetime.now())
        ]

        TransactionMemoryRepository.save_transactions(transactions)

        result = TransactionMemoryRepository.get_transactions()

        #asserts ...
