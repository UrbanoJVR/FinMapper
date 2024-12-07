from datetime import datetime
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from flask_babel import format_datetime

from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@pytest.fixture(scope='function')
def given_a_transaction(client) -> Transaction:
    CategoryRepository().save(Category(name="Category for transaction", description="Category description"))
    category_id = CategoryRepository().get_by_name("Category for transaction").id
    client.post('/transactions/add',
                data=dict(amount=100, concept='concept', date='2024-12-01', category_id=category_id))
    return TransactionRepository().get_by_id(1)


@pytest.fixture(scope='function')
def given_a_transaction_with_specific_date(client, date: datetime.date) -> Transaction:
    CategoryRepository().save(Category(name="Category for transaction", description="Category description"))
    category = CategoryRepository().get_by_name("Category for transaction")
    TransactionRepository().save(
        Transaction(transaction_date=date, amount=Decimal(100), concept="Concept", category=category))
    return TransactionRepository().get_by_id(1)


def count_transactions_in_table(client, month: int, year: int) -> int:
    html = BeautifulSoup(client.get(f'/movements/{month}/{year}').data, 'html.parser')
    table = html.find('table', {'class': 'table'})

    # -1 because first row is allways header
    return len(table.find_all('tr')) - 1


def transaction_exists(client, transaction: Transaction) -> bool:
    response = client.get(f'/movements/{transaction.transaction_date.month}/{transaction.transaction_date.year}')
    assert response.status_code == 200
    return _transaction_in_table(response.data, transaction)


def transaction_not_exists(client, transaction: Transaction) -> bool:
    response = client.get(f'/movements/{transaction.transaction_date.month}/{transaction.transaction_date.year}')
    assert response.status_code == 200
    return not _transaction_in_table(response.data, transaction)


def _transaction_in_table(response_data: bytes, transaction: Transaction) -> bool:
    html_parser = BeautifulSoup(response_data, 'html.parser')

    formatted_date: str = format_datetime(transaction.transaction_date, 'EEEE, dd-MM-yyyy')
    formatted_amount: str = f"{transaction.amount:.2f}"
    category_name: str = transaction.category.name if transaction.category else ""
    transaction_data = [formatted_date, transaction.concept, formatted_amount, category_name]

    table = html_parser.find('table', {'class': 'table'})
    assert table is not None

    rows = table.find_all('tr')
    for row in rows:
        cells_text = [cell.text.strip() for cell in row.find_all('td')]
        if all(data in cells_text for data in transaction_data):
            return True

    return False
