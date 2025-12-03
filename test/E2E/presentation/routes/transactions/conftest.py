from datetime import datetime
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup
from flask_babel import format_datetime

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@pytest.fixture(scope='function')
def given_a_transaction(client) -> Transaction:
    CategoryRepository().save(Category(name="Category for transaction", description="Category description"))
    category_id = CategoryRepository().get_by_name("Category for transaction").id
    client.post('/transactions/add',
                data=dict(amount=100, concept='concept', comments='comments', date='2024-12-01', category_id=category_id))
    return TransactionRepository().get_by_id(1)


@pytest.fixture(scope='function')
def given_a_transaction_with_specific_date(client, date: datetime.date) -> Transaction:
    """Fixture que crea una transacción con fecha específica. Por defecto usa EXPENSE."""
    return _create_transaction_with_date_and_type(client, date, TransactionType.EXPENSE)


@pytest.fixture(scope='function')
def given_a_transaction_with_specific_date_and_type(client, date: datetime.date, transaction_type: TransactionType) -> Transaction:
    """Fixture que crea una transacción con fecha y tipo específicos."""
    return _create_transaction_with_date_and_type(client, date, transaction_type)


def _create_transaction_with_date_and_type(client, date: datetime.date, transaction_type: TransactionType) -> Transaction:
    """Función helper para crear transacciones con fecha y tipo específicos."""
    CategoryRepository().save(Category(name="Category for transaction", description="Category description"))
    category = CategoryRepository().get_by_name("Category for transaction")
    TransactionRepository().save(
        Transaction(transaction_date=TransactionDate(date), amount=Decimal(100), concept="Concept", type=transaction_type, category=category))
    return TransactionRepository().get_by_id(1)


def count_transactions_in_table(client, month: int, year: int) -> int:
    html = BeautifulSoup(client.get(f'/movements/{month}/{year}').data, 'html.parser')
    table = html.find('table', {'class': 'table'})

    # Get all rows except header
    rows = table.find_all('tr')[1:]  # Skip header row
    
    # Filter out the "No transactions found" row if it exists
    transaction_rows = []
    for row in rows:
        # Check if this row contains the "No transactions found" message
        if 'No transactions found' not in row.get_text():
            transaction_rows.append(row)
    
    return len(transaction_rows)


def transaction_exists(client, transaction: Transaction) -> bool:
    response = client.get(f'/movements/{transaction.transaction_date.value.month}/{transaction.transaction_date.value.year}')
    assert response.status_code == 200
    return _transaction_in_table(response.data, transaction)


def transaction_not_exists(client, transaction: Transaction) -> bool:
    response = client.get(f'/movements/{transaction.transaction_date.value.month}/{transaction.transaction_date.value.year}')
    assert response.status_code == 200
    return not _transaction_in_table(response.data, transaction)


def _transaction_in_table(response_data: bytes, transaction: Transaction) -> bool:
    html_parser = BeautifulSoup(response_data, 'html.parser')
    print(html_parser.prettify())

    # Format data to match what's actually displayed in the new table design
    formatted_date_short: str = format_datetime(transaction.transaction_date.value, 'dd/MM/yyyy')
    formatted_date_day: str = format_datetime(transaction.transaction_date.value, 'EEEE')
    formatted_amount: str = f"{transaction.amount.value:.2f}"
    category_name: str = transaction.category.name if transaction.category else ""
    
    # Build transaction data to search for
    transaction_data = [transaction.concept, formatted_amount]
    if transaction.comments:
        transaction_data.append(transaction.comments)
    if category_name:
        transaction_data.append(category_name)

    table = html_parser.find('table', {'class': 'table'})
    assert table is not None

    rows = table.find_all('tr')
    for row in rows:
        # Get all text content from the row, including nested elements
        row_text = row.get_text()
        
        # Check if the row contains the date (either format) and all other transaction data
        date_found = (formatted_date_short in row_text or 
                     formatted_date_day in row_text)
        
        if date_found and all(data in row_text for data in transaction_data if data):
            return True

    return False
