from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

from app.src.domain.category import Category
from app.src.domain.transaction.vo.transaction_date import TransactionDate


@dataclass(frozen=True)
class Transaction:

    transaction_date: TransactionDate
    amount: Decimal
    concept: str
    comments: str | None = None
    category: Category | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.transaction_date, TransactionDate):
            raise TypeError("transaction_date must be a TransactionDate")

        if not isinstance(self.amount, Decimal):
            raise TypeError("amount must be a Decimal")

        if not self.concept or self.concept.strip() == "":
            raise ValueError("concept cannot be empty")

    @staticmethod
    def create(
        transaction_date: TransactionDate,
        amount: Decimal,
        concept: str,
        comments: str | None = None,
        category: Category | None = None
    ) -> Transaction:
        return Transaction(
            transaction_date,
            amount,
            concept,
            comments,
            category,
            None
        )

    @staticmethod
    def builder() -> Transaction.Builder:
        return Transaction.Builder()

    def to_builder(self) -> Transaction.Builder:
        return (
            Transaction.builder()
            .transaction_date(self.transaction_date)
            .amount(self.amount)
            .concept(self.concept)
            .comments(self.comments)
            .category(self.category)
            .id(self.id)
        )

    class Builder:
        _transaction_date: TransactionDate | None
        _amount: Decimal | None
        _concept: str | None
        _comments: str | None
        _category: Category | None
        _id: int | None

        def __init__(self) -> None:
            self._transaction_date = None
            self._amount = None
            self._concept = None
            self._comments = None
            self._category = None
            self._id = None

        def transaction_date(self, value: TransactionDate) -> Transaction.Builder:
            self._transaction_date = value
            return self

        def amount(self, value: Decimal) -> Transaction.Builder:
            self._amount = value
            return self

        def concept(self, value: str) -> Transaction.Builder:
            self._concept = value
            return self

        def comments(self, value: str | None) -> Transaction.Builder:
            self._comments = value
            return self

        def category(self, value: Category | None) -> Transaction.Builder:
            self._category = value
            return self

        def id(self, value: int | None) -> Transaction.Builder:
            self._id = value
            return self

        def build(self) -> Transaction:
            return Transaction(
                self._transaction_date,   # type: ignore
                self._amount,             # type: ignore
                self._concept,            # type: ignore
                self._comments,
                self._category,
                self._id
            )

    def change_transaction_date(self, value: TransactionDate) -> Transaction:
        return self.to_builder().transaction_date(value).build()

    def change_amount(self, value: Decimal) -> Transaction:
        return self.to_builder().amount(value).build()

    def change_concept(self, value: str) -> Transaction:
        return self.to_builder().concept(value).build()

    def change_comments(self, value: str | None) -> Transaction:
        return self.to_builder().comments(value).build()

    def change_category(self, value: Category | None) -> Transaction:
        return self.to_builder().category(value).build()

    def change_id(self, value: int | None) -> Transaction:
        return self.to_builder().id(value).build()

    def update(
        self,
        transaction_date: TransactionDate,
        amount: Decimal,
        concept: str,
        comments: str | None,
        category: Category | None
    ) -> Transaction:
        return (
            self.to_builder()
            .transaction_date(transaction_date)
            .amount(amount)
            .concept(concept)
            .comments(comments)
            .category(category)
            .build()
        )
