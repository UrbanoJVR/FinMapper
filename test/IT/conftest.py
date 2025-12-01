from datetime import date
from decimal import Decimal

import pytest

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@pytest.fixture(scope='function')
def save_transactions_from_different_months_and_categories(db_test_it):
    _create_five_categories()
    category_repository = CategoryRepository()
    transaction_repository = TransactionRepository()

    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(100.50)), transaction_date=TransactionDate(date(2025, 1, 1)), concept="Random concept", category=category_repository.get_by_name('Category 0')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(999.25)), transaction_date=TransactionDate(date(2025, 1, 5)), concept="Random concept", category=category_repository.get_by_name('Category 0')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(199.75)), transaction_date=TransactionDate(date(2025, 1, 20)), concept="Random concept", category=category_repository.get_by_name('Category 0')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(105.75)), transaction_date=TransactionDate(date(2025, 2, 26)), concept="Random concept", category=category_repository.get_by_name('Category 0')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(13.95)), transaction_date=TransactionDate(date(2025, 4, 2)), concept="Random concept", category=category_repository.get_by_name('Category 0')))

    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(199.95)), transaction_date=TransactionDate(date(2025, 1, 2)), concept="Random concept", category=category_repository.get_by_name('Category 1')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(50.76)), transaction_date=TransactionDate(date(2025, 1, 7)), concept="Random concept", category=category_repository.get_by_name('Category 1')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(80.01)), transaction_date=TransactionDate(date(2025, 1, 18)), concept="Random concept", category=category_repository.get_by_name('Category 1')))

    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(12.50)), transaction_date=TransactionDate(date(2025, 1, 1)), concept="Random concept", category=category_repository.get_by_name('Category 2')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(99.02)), transaction_date=TransactionDate(date(2025, 7, 5)), concept="Random concept", category=category_repository.get_by_name('Category 2')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(764.86)), transaction_date=TransactionDate(date(2025, 10, 28)), concept="Random concept", category=category_repository.get_by_name('Category 2')))

    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(67.93)), transaction_date=TransactionDate(date(2025, 2, 15)), concept="Random concept", category=category_repository.get_by_name('Category 3')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(23.85)), transaction_date=TransactionDate(date(2025, 9, 12)), concept="Random concept", category=category_repository.get_by_name('Category 3')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(837.08)), transaction_date=TransactionDate(date(2025, 12, 6)), concept="Random concept", category=category_repository.get_by_name('Category 3')))

    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(874.01)), transaction_date=TransactionDate(date(2024, 11, 11)), concept="Random concept", category=category_repository.get_by_name('Category 4')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(5789.06)), transaction_date=TransactionDate(date(2025, 10, 8)), concept="Random concept", category=category_repository.get_by_name('Category 4')))
    transaction_repository.save(Transaction(amount=TransactionAmount(Decimal(2314.99)), transaction_date=TransactionDate(date(2026, 6, 6)), concept="Random concept", category=category_repository.get_by_name('Category 4')))


def _create_five_categories() -> list[Category]:
    category_repository = CategoryRepository()

    for i in range(5):
        category_repository.save(Category(name=f'Category {i}', description=f'Description {i}'))

    return category_repository.get_all()
