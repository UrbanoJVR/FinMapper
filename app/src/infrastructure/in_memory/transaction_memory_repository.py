from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from flask import session

from app.src.domain.transaction import Transaction


class TransactionMemoryRepository:

    @staticmethod
    def save_transactions(transactions: list[Transaction]):
        transactions_dict = []

        for transaction in transactions:
            transactions_dict.append(TmpTransaction.from_domain(transaction).to_dict())

        session['transactions'] = transactions_dict

    @staticmethod
    def get_transactions() -> list[Transaction]:
        tmp_transactions: list[dict] = session.get('transactions', [])
        transactions: list[Transaction] = []

        for tmp_transaction in tmp_transactions:
            transactions.append(TmpTransaction.from_dict_to_domain(tmp_transaction))

        return transactions

    @staticmethod
    def clear():
        session.pop('transactions')


@dataclass
class TmpTransaction:
    amount: str
    date: str
    concept: str

    @staticmethod
    def from_domain(transaction: Transaction):
        return TmpTransaction(str(transaction.amount), str(transaction.transaction_date), str(transaction.concept))

    def to_domain(self) -> Transaction:
        return Transaction(
            amount=Decimal(self.amount.replace(',', '.')),
            transaction_date=datetime.fromisoformat(self.date).date(),
            concept=self.concept
        )

    def to_dict(self) -> dict:

        # noinspection PyTypeChecker
        return asdict(self)

    @staticmethod
    def from_dict_to_domain(data: dict) -> Transaction:
        return TmpTransaction(**data).to_domain()