from decimal import Decimal

from faker import Faker

from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand


class UpdateTransactionCommandMother:
    _faker = Faker()

    def random(self):
        return UpdateTransactionCommand(
            concept=self._faker.sentence(),
            comments=self._faker.sentence(),
            amount=Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True))),
            date=self._faker.date_object(),
            transaction_id=self._faker.random_number(),
            category_id=self._faker.random_number()
        )

    def random_with_empty_category(self) -> UpdateTransactionCommand:
        return UpdateTransactionCommand(
            concept=self._faker.sentence(),
            comments=self._faker.sentence(),
            amount=Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True))),
            date=self._faker.date_object(),
            transaction_id=self._faker.random_number(),
            category_id=None
        )

    def random_with_transaction_id_and_category_id(self, transaction_id:int, category_id: int) -> UpdateTransactionCommand:
        return UpdateTransactionCommand(
            concept=self._faker.sentence(),
            comments=self._faker.sentence(),
            amount=Decimal(str(self._faker.pydecimal(left_digits=3, right_digits=2, positive=True))),
            date=self._faker.date_object(),
            transaction_id=transaction_id,
            category_id=category_id
        )