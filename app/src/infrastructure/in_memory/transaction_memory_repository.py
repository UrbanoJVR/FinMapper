from decimal import Decimal

from flask import session

from app.src.domain.transaction import Transaction
from app.src.shared.date_utils import str_to_date


class TransactionMemoryRepository:

    @staticmethod
    def save_transactions(transactions: list[Transaction]):
        session['transactions'] = transactions

    # @staticmethod
    # def get_transactions() -> list[Transaction]:
    #     tmp_transactions = session['transactions']
    #     transactions: list[Transaction] = []
    #
    #     for transaction in tmp_transactions:
    #         transactions.append(
    #             Transaction(id=None,
    #                         category=None,
    #                         amount=transaction.amount,
    #                         concept=transaction.concept,
    #                         transaction_date=transaction.transaction_date))
    #
    #     return transactions

    @staticmethod
    def get_transactions() -> list[Transaction]:
        return session['transactions']

    @staticmethod
    def clear():
        session.pop('transactions')
