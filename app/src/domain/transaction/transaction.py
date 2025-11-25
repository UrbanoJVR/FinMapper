from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal

from app.src.domain.category import Category


@dataclass(frozen=True)
class Transaction:

    transaction_date: date
    amount: Decimal
    concept: str
    comments: str | None = None
    category: Category | None = None
    id: int | None = None

    @staticmethod
    def _validate(transaction_date: date, amount: Decimal, concept: str):
        if transaction_date is None:
            raise ValueError("transaction_date cannot be null")

        if amount is None:
            raise ValueError("amount cannot be null")

        if not concept or concept.strip() == "":
            raise ValueError("concept cannot be empty")

    @staticmethod
    def create(
        transaction_date: date,
        amount: Decimal,
        concept: str,
        comments: str | None = None,
        category: Category | None = None
    ) -> "Transaction":

        Transaction._validate(transaction_date, amount, concept)

        return Transaction(
            transaction_date=transaction_date,
            amount=amount,
            concept=concept,
            comments=comments,
            category=category,
            id=None
        )

    def change_transaction_date(self, transaction_date: date) -> "Transaction":
        Transaction._validate(transaction_date, self.amount, self.concept)
        return replace(self, transaction_date=transaction_date)

    def change_amount(self, amount: Decimal) -> "Transaction":
        Transaction._validate(self.transaction_date, amount, self.concept)
        return replace(self, amount=amount)

    def change_concept(self, concept: str) -> "Transaction":
        Transaction._validate(self.transaction_date, self.amount, concept)
        return replace(self, concept=concept)

    def change_comments(self, comments: str | None) -> "Transaction":
        return replace(self, comments=comments)

    def change_category(self, category: Category | None) -> "Transaction":
        return replace(self, category=category)

    def change_id(self, id_value: int | None) -> "Transaction":
        return replace(self, id=id_value)

    def update(
        self,
        transaction_date: date,
        amount: Decimal,
        concept: str,
        comments: str | None,
        category: Category | None
    ) -> "Transaction":

        Transaction._validate(transaction_date, amount, concept)

        return replace(
            self,
            transaction_date=transaction_date,
            amount=amount,
            concept=concept,
            comments=comments,
            category=category
        )
