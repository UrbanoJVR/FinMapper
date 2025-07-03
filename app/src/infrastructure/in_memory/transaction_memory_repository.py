from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from flask import session

from app.src.domain.category import Category
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
        transactions: list[Transaction] = [TmpTransaction.from_dict_to_domain(tmp) for tmp in tmp_transactions]

        return sorted(transactions, key=lambda t: t.transaction_date, reverse=True)

    @staticmethod
    def clear():
        session.pop('transactions', None)


@dataclass
class TmpTransaction:
    amount: str
    date: str
    concept: str
    comments: str
    category_name: str
    category_id: int

    @staticmethod
    def from_domain(transaction: Transaction):
        return TmpTransaction(str(transaction.amount),
                              str(transaction.transaction_date),
                              str(transaction.concept),
                              str(transaction.comments),
                              str(transaction.category.name if transaction.category else None),
                              transaction.category.id if transaction.category else None)

    def to_domain(self) -> Transaction:
        return Transaction(
            amount=Decimal(self.amount.replace(',', '.')),
            transaction_date=datetime.fromisoformat(self.date).date(),
            concept=self.concept,
            comments=self.comments if self.comments not in [None, "", "None", "nan"] else None,
            category=Category(name=self.category_name, id=self.category_id)
            if self.category_name not in [None, "", "None", "null", "nan"] else None
        )

    def to_dict(self) -> dict:
        # noinspection PyTypeChecker
        return asdict(self)

    @staticmethod
    def from_dict_to_domain(data: dict) -> Transaction:
        return TmpTransaction(**data).to_domain()
