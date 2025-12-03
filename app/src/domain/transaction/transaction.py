from __future__ import annotations

from dataclasses import dataclass

from app.src.domain.category import Category
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType


@dataclass(frozen=True)
class Transaction:
    transaction_date: TransactionDate
    amount: TransactionAmount
    concept: str
    type: TransactionType
    comments: str | None = None
    category: Category | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.transaction_date, TransactionDate):
            raise TypeError("transaction_date must be a TransactionDate type")

        if self.transaction_date is None:
            raise TypeError("transaction_date cannot be empty")

        if not isinstance(self.amount, TransactionAmount):
            raise TypeError("amount must be TransactionAmount type")

        if self.amount is None:
            raise TypeError("amount cannot be empty")

        if not self.concept or self.concept.strip() == "":
            raise ValueError("concept cannot be empty")

        if not type:
            raise TypeError("type cannot be empty")

    @staticmethod
    def create(
            transaction_date: TransactionDate,
            amount: TransactionAmount,
            concept: str,
            type: TransactionType,
            comments: str | None = None,
            category: Category | None = None
    ) -> Transaction:
        return Transaction(
            transaction_date,
            amount,
            concept,
            type,
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
            .type(self.type)
            .comments(self.comments)
            .category(self.category)
            .id(self.id)
        )

    class Builder:
        _transaction_date: TransactionDate | None
        _amount: TransactionAmount | None
        _concept: str | None
        _type: TransactionType | None
        _comments: str | None
        _category: Category | None
        _id: int | None

        def __init__(self) -> None:
            self._transaction_date = None
            self._amount = None
            self._concept = None
            self._type = None
            self._comments = None
            self._category = None
            self._id = None

        def transaction_date(self, value: TransactionDate) -> Transaction.Builder:
            self._transaction_date = value
            return self

        def amount(self, value: TransactionAmount) -> Transaction.Builder:
            self._amount = value
            return self

        def concept(self, value: str) -> Transaction.Builder:
            self._concept = value
            return self

        def type(self, value: TransactionType) -> Transaction.Builder:
            self._type = value
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
                self._transaction_date,
                self._amount,
                self._concept,
                self._type,
                self._comments,
                self._category,
                self._id
            )

    def change_category(self, value: Category | None) -> Transaction:
        return self.to_builder().category(value).build()

    def update(
            self,
            transaction_date: TransactionDate,
            amount: TransactionAmount,
            concept: str,
            type: TransactionType,
            comments: str | None,
            category: Category | None
    ) -> Transaction:
        return (
            self.to_builder()
            .transaction_date(transaction_date)
            .amount(amount)
            .concept(concept)
            .type(type)
            .comments(comments)
            .category(category)
            .build()
        )
