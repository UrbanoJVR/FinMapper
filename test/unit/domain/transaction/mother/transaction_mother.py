from datetime import date
from decimal import Decimal

from faker import Faker

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from test.unit.domain.category.mother.category_mother import CategoryMother


class TransactionMother:
    _faker = Faker()
    _category_mother = CategoryMother()

    def random(self):
        return Transaction(
            transaction_date=TransactionDate(self._faker.date_object()),
            amount=TransactionAmount(
                Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True)))),
            concept=self._faker.sentence(),
            comments=self._faker.sentence(),
            category=self._category_mother.random(),
            id=self._faker.random_number(),
        )

    def random_with_id(self, transaction_id: int) -> Transaction:
        return self.random().to_builder().id(transaction_id).build()

    def random_with_empty_category_and_id(self, transaction_id: int) -> Transaction:
        return self.random_with_empty_category().to_builder().id(transaction_id).build()

    def random_with_empty_category(self):
        return Transaction(
            transaction_date=TransactionDate(self._faker.date_object()),
            amount=TransactionAmount(
                Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True)))),
            concept=self._faker.sentence(),
            comments=self._faker.sentence(),
            category=None,
            id=self._faker.random_number(),
        )

    def random_with_date_and_category_and_id(self, transaction_date: date, category: Category,
                                             transaction_id: int) -> Transaction:
        return (
            Transaction.builder()
            .transaction_date(TransactionDate(transaction_date))
            .amount(TransactionAmount(Decimal("100.00")))
            .concept("Concept 1")
            .comments(None)
            .category(category)
            .id(transaction_id)
            .build()
        )
