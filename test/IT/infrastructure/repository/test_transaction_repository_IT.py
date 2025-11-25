from datetime import date
from decimal import Decimal
from typing import List

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestTransactionRepositoryIT:

    def setup_method(self):
        self.sut = TransactionRepository()
        self.category_repository = CategoryRepository()

    def test_when_create_should_autoincrement_id(self, db_test_it):
        transaction = Transaction(transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept")

        self.sut.save(transaction)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == 1

    def test_when_save_should_save_and_find_should_find_saved(self, db_test_it):
        transaction = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept")
        self.sut.save(transaction)

        transactions = self.sut.find_all()

        assert len(transactions) == 1
        assert transactions[0].id == transaction.id
        assert transactions[0].amount == transaction.amount

    def test_when_save_and_array_then_should_find(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept")
        transactions = [transaction1, transaction2]

        self.sut.save_transactions(transactions)

        transactions = self.sut.find_all()
        assert len(transactions) == 2
        assert transactions[0].id == 1
        assert transactions[0].amount == transactions[0].amount
        assert transactions[1].id == 2
        assert transactions[1].amount == transactions[1].amount

    def test_whe_delete_by_id_then_not_find(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept")
        transactions = [transaction1, transaction2]
        self.sut.save_transactions(transactions)

        self.sut.delete_by_id(transaction1.id)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == 2
        assert transactions[0].amount == transaction2.amount

    def test_when_update_then_save_new_values_and_find_them(self, db_test_it):
        origin_transaction = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                         category=None, concept="Concept")
        edited_transaction = Transaction(id=1, transaction_date=TransactionDate(date(2025, 12, 1)), amount=Decimal(50),
                                         category=None, concept="New Concept")
        self.sut.save(origin_transaction)

        self.sut.update(edited_transaction)

        transactions = self.sut.find_all()
        assert len(transactions) == 1
        assert transactions[0].id == origin_transaction.id
        assert transactions[0].id == edited_transaction.id
        assert transactions[0].amount == edited_transaction.amount
        assert transactions[0].transaction_date.value == edited_transaction.transaction_date.value
        assert transactions[0].concept == edited_transaction.concept

    def test_whe_get_by_month_year_should_works(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept")
        self.sut.save(transaction1)
        self.sut.save(transaction2)

        transactions = self.sut.get_by_month_year(12, 2024)

        assert len(transactions) == 1
        assert transactions[0].id == transaction1.id
        assert transactions[0].amount == transaction1.amount

    def test_when_get_by_month_year_and_category_should_works(self, save_transactions_from_different_months_and_categories):
        category_zero = self.category_repository.get_by_name('Category 0')
        expected_transactions = [
            Transaction(amount=Decimal(199.75), transaction_date=TransactionDate(date(2025, 1, 20)), concept="Random concept",
                        category=self.category_repository.get_by_name('Category 0'), id=3),
            Transaction(amount=Decimal(999.25), transaction_date=TransactionDate(date(2025, 1, 5)), concept="Random concept",
                        category=self.category_repository.get_by_name('Category 0'), id=2),
            Transaction(amount=Decimal(100.50), transaction_date=TransactionDate(date(2025, 1, 1)), concept="Random concept",
                        category=self.category_repository.get_by_name('Category 0'), id=1)
        ]

        result = self.sut.get_by_month_year_and_category_id(1, 2025, category_zero.id)

        assert result == expected_transactions

    def test_whe_get_by_id_should_works(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept")
        self.sut.save_transactions([transaction1, transaction2])

        transaction_result = self.sut.get_by_id(transaction2.id)

        assert transaction_result.amount == transaction2.amount
        assert transaction_result.id == transaction2.id

    def test_when_get_last_uncategorized_should_return_last_uncategorized_transaction_by_date(self, db_test_it):
        category = Category(id=1, name="Category name", description="Category description")
        self.category_repository.save(category)
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept 2")
        transaction3 = Transaction(id=3, transaction_date=TransactionDate(date(2024, 12, 2)), amount=Decimal(50),
                                   category=category, concept="Concept 3")
        self.sut.save_transactions([transaction1, transaction2, transaction3])

        transaction_result: Transaction = self.sut.get_last_uncategorized()

        assert transaction_result.id == transaction1.id
        assert transaction_result.amount == transaction1.amount
        assert transaction_result.concept == transaction1.concept
        assert transaction_result.category is None

    def test_get_uncategorized_by_month_year(self, db_test_it):
        category = Category(id=1, name="Category name", description="Category description")
        self.category_repository.save(category)
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                   category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 11, 1)), amount=Decimal(50),
                                   category=None, concept="Concept 2")
        transaction3 = Transaction(id=3, transaction_date=TransactionDate(date(2024, 12, 2)), amount=Decimal(50),
                                   category=category, concept="Concept 3")
        self.sut.save_transactions([transaction1, transaction2, transaction3])

        result: List[Transaction] = self.sut.get_uncategorized_by_month_year(12, 2024)

        assert len(result) == 1
        assert result[0].id == transaction1.id
        assert result[0].amount == transaction1.amount
        assert result[0].category is None

    def test_find_first_by_category_id_success(self, db_test_it):
        category = Category(id=2, name="Category name", description="Category description")
        self.category_repository.save(category)
        transaction = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=category, concept="Concept 1")
        self.sut.save(transaction)

        result = self.sut.find_first_by_category_id(category.id)

        assert result == transaction

    def test_find_first_by_category_id_return_none(self, db_test_it):
        category = Category(id=999, name="Non-existent category", description="Category description")
        self.category_repository.save(category)
        
        result = self.sut.find_first_by_category_id(category.id)
        
        assert result is None

    def test_count_by_category_id_should_return_zero(self, db_test_it):
        result = self.sut.count_by_category_id(1)

        assert result == 0

    def test_count_by_category_id_should_return_one(self, db_test_it):
        category = Category(id=1, name="Category name", description="Category description")
        self.category_repository.save(category)
        transaction = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=category, concept="Concept 1")
        self.sut.save(transaction)

        result = self.sut.count_by_category_id(1)

        assert result == 1

    def test_given_no_transactions_when_request_years_with_transactions_then_return_empty_list(self, db_test_it):
        result = self.sut.get_years_with_transactions()

        assert result == []

    def test_given_a_year_with_more_than_one_transactions_when_reqeust_years_with_transactions_then_return_one_year_list(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        self.sut.save(transaction1)
        self.sut.save(transaction2)

        result = self.sut.get_years_with_transactions()

        assert len(result) == 1
        assert result[0] == 2024

    def test_given_different_years_with_transactions_then_return_correct_list(self, db_test_it):
        transaction1 = Transaction(id=1, transaction_date=TransactionDate(date(2024, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        transaction2 = Transaction(id=2, transaction_date=TransactionDate(date(2025, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        transaction3 = Transaction(id=3, transaction_date=TransactionDate(date(2025, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        transaction4 = Transaction(id=4, transaction_date=TransactionDate(date(2023, 12, 1)), amount=Decimal(100),
                                  category=None, concept="Concept 1")
        self.sut.save(transaction1)
        self.sut.save(transaction2)
        self.sut.save(transaction3)
        self.sut.save(transaction4)

        result = self.sut.get_years_with_transactions()

        assert len(result) == 3
        assert result[0] == 2023
        assert result[1] == 2024
        assert result[2] == 2025

    def test_get_by_year_returns_transactions_for_specific_year(self, db_test_it):
        transaction1 = Transaction(transaction_date=TransactionDate(date(2024, 1, 15)), amount=Decimal("100.00"),
                                  category=None, concept="Concept 1")
        transaction2 = Transaction(transaction_date=TransactionDate(date(2024, 6, 20)), amount=Decimal("200.00"),
                                  category=None, concept="Concept 2")
        transaction3 = Transaction(transaction_date=TransactionDate(date(2023, 12, 31)), amount=Decimal("300.00"),
                                  category=None, concept="Concept 3")
        transaction4 = Transaction(transaction_date=TransactionDate(date(2025, 1, 1)), amount=Decimal("400.00"),
                                  category=None, concept="Concept 4")

        self.sut.save(transaction1)
        self.sut.save(transaction2)
        self.sut.save(transaction3)
        self.sut.save(transaction4)

        result = self.sut.get_by_year(2024)

        assert len(result) == 2
        assert result[0].concept == "Concept 2"  # More recent first
        assert result[1].concept == "Concept 1"
        assert all(t.transaction_date.value.year == 2024 for t in result)

    def test_get_by_year_returns_empty_list_when_no_transactions_for_year(self, db_test_it):
        transaction = Transaction(transaction_date=TransactionDate(date(2023, 1, 1)), amount=Decimal("100.00"),
                                 category=None, concept="Concept 1")
        self.sut.save(transaction)

        result = self.sut.get_by_year(2024)

        assert len(result) == 0