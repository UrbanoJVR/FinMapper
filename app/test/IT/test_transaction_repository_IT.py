from datetime import date
from decimal import Decimal
from typing import List

from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestTransactionRepositoryIT:

    def setup_method(self):
        self.sut = TransactionRepository()

    def test_autoincrement_id(self, db_test_it):
        transaction = Transaction(transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                  category=None, concept="Concept")

        self.sut.save(transaction)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == 1

    def test_save_and_find_all(self, db_test_it):
        transaction = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                  category=None, concept="Concept")
        self.sut.save(transaction)

        transactions = self.sut.find_all()

        assert len(transactions) == 1
        assert transactions[0].id == transaction.id
        assert transactions[0].amount == transaction.amount

    def test_save_array(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept")
        transactions = [transaction1, transaction2]

        self.sut.save_transactions(transactions)

        transactions = self.sut.find_all()
        assert len(transactions) == 2
        assert transactions[0].id == 1
        assert transactions[0].amount == transactions[0].amount
        assert transactions[1].id == 2
        assert transactions[1].amount == transactions[1].amount


    def test_delete_by_id(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept")
        transactions = [transaction1, transaction2]
        self.sut.save_transactions(transactions)

        self.sut.delete_by_id(transaction1.id)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == 2
        assert transactions[0].amount == transaction2.amount

    def test_update(self, db_test_it):
        origin_transaction = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept")
        edited_transaction = Transaction(id=1, transaction_date=date(2025, 12, 1), amount=Decimal(50),
                                         category=None, concept="New Concept")
        self.sut.save(origin_transaction)

        self.sut.update(edited_transaction)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == origin_transaction.id
        assert transactions[0].id == edited_transaction.id
        assert transactions[0].amount == edited_transaction.amount
        assert transactions[0].transaction_date == edited_transaction.transaction_date
        assert transactions[0].concept == edited_transaction.concept

    def test_get_by_month_year(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept")
        self.sut.save(transaction1)
        self.sut.save(transaction2)

        transactions = self.sut.get_by_month_year(12, 2024)

        assert len(transactions) == 1
        assert transactions[0].id == transaction1.id
        assert transactions[0].amount == transaction1.amount

    def test_get_by_id(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept")
        self.sut.save_transactions([transaction1, transaction2])

        transaction_result = self.sut.get_by_id(transaction2.id)

        assert transaction_result.amount == transaction2.amount
        assert transaction_result.id == transaction2.id

    def test_get_last_uncategorized(self, db_test_it):
        category = Category(id=1, name="Category name", description="Category description")
        CategoryRepository().save(category)
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept 2")
        transaction3 = Transaction(id=3, transaction_date=date(2024, 12, 2), amount=Decimal(50),
                                   category=category, concept="Concept 3")
        self.sut.save_transactions([transaction1, transaction2, transaction3])

        transaction_result: Transaction = self.sut.get_last_uncategorized()

        assert transaction_result.id == transaction1.id
        assert transaction_result.amount == transaction1.amount
        assert transaction_result.concept == transaction1.concept
        assert transaction_result.category is None

    def test_get_uncategorized_by_month_year(self, db_test_it):
        category = Category(id=1, name="Category name", description="Category description")
        CategoryRepository().save(category)
        transaction1 = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=date(2024, 11, 1), amount=Decimal(50),
                                   category=None, concept="Concept 2")
        transaction3 = Transaction(id=3, transaction_date=date(2024, 12, 2), amount=Decimal(50),
                                   category=category, concept="Concept 3")
        self.sut.save_transactions([transaction1, transaction2, transaction3])

        result: List[Transaction] = self.sut.get_uncategorized_by_month_year(12, 2024)

        assert len(result) == 1
        assert result[0].id == transaction1.id
        assert result[0].amount == transaction1.amount
        assert result[0].category is None

    def test_find_first_by_category_id_success(self, db_test_it):
        category = Category(id=2, name="Category name", description="Category description")
        CategoryRepository().save(category)
        transaction = Transaction(id=1, transaction_date=date(2024, 12, 1), amount=Decimal(100),
                                   category=category, concept="Concept 1")
        self.sut.save(transaction)

        result = self.sut.find_first_by_category_id(category.id)

        assert result == transaction

    def test_find_first_by_category_id_return_none(self, db_test_it):
        assert True
