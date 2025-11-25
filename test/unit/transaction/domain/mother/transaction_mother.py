from decimal import Decimal

from faker import Faker

from app.src.domain.transaction.transaction import Transaction


class TransactionMother:
    _faker = Faker()

    @staticmethod
    def random():
        return Transaction(
            transaction_date=TransactionMother._faker.date_object(),
            amount=Decimal(str(TransactionMother._faker.pydecimal(left_digits=3, right_digits=2, positive=True))),
            concept=TransactionMother._faker.sentence(),
            comments=None,
            category=None,
            id=None
        )