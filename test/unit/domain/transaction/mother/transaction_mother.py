from decimal import Decimal

from faker import Faker

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType
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
            type=self._faker.random_element(list(TransactionType)),
            comments=self._faker.sentence(),
            category=self._category_mother.random(),
            id=self._faker.random_number(),
        )

    def random_with_id(self, transaction_id: int) -> Transaction:
        return self.random().to_builder().id(transaction_id).build()

    def random_with_empty_category_and_id(self, transaction_id: int) -> Transaction:
        return self.random_expense_with_empty_category().to_builder().id(transaction_id).build()

    def random_expense_with_empty_category(self):
        return Transaction(
            transaction_date=TransactionDate(self._faker.date_object()),
            amount=TransactionAmount(
                Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True)))),
            concept=self._faker.sentence(),
            type=TransactionType.EXPENSE,
            comments=self._faker.sentence(),
            category=None,
            id=self._faker.random_number(),
        )

    def random_income_with_empty_category(self):
        return (self.random().to_builder()
                .category(None)
                .type(TransactionType.INCOME)
                .build())
