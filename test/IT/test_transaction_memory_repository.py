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

class TestTransactionMemoryRepository:

    def setup_method(self):
        self.sut = TransactionMemoryRepository()

    def test_save_and_get_transactions(self, flask_request_context):
        transactions = [
            Transaction(id=None, category=None, amount=Decimal(100), concept="Concept 1",
                        transaction_date=datetime.now()),
            Transaction(id=None, category=None, amount=Decimal(200), concept="Concept 2",
                        transaction_date=datetime.now())
        ]

        # Guardar las transacciones en la sesión
        TransactionMemoryRepository.save_transactions(transactions)

        # Recuperar las transacciones desde la sesión
        result = TransactionMemoryRepository.get_transactions()

        # Verificar que las transacciones recuperadas coincidan con las originales
        assert len(result) == len(transactions)
        assert result[0].amount == transactions[0].amount
        assert result[1].concept == transactions[1].concept

    # def test_save_and_get_transactions(self):
    #     transactions = [Transaction(id=None, category=None, amount=Decimal(100), concept="Concept 1",
    #                                 transaction_date=datetime.now()),
    #                     Transaction(id=None, category=None, amount=Decimal(200), concept="Concept 2",
    #                                 transaction_date=datetime.now())]
    #
    #     self.sut.save_transactions(transactions)
    #     result = self.sut.get_transactions()
    #
    #     assert result == transactions

