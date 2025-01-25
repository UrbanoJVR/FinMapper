from datetime import datetime
from decimal import Decimal

import pytest

from app.src.domain.category import Category
from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@pytest.fixture(scope='function')
def given_a_category(client) -> Category:
    client.post('/categories/create', data=dict(name='TestCategory', description='Test description'))
    return CategoryRepository().get_by_name('TestCategory')


@pytest.fixture(scope='function')
def given_multiple_categories(client):
    client.post('/categories/create', data=dict(name='Category1', description='Description 1'))
    client.post('/categories/create', data=dict(name='Category2', description='Description 2'))
    client.post('/categories/create', data=dict(name='Category3', description='Description 3'))

    return CategoryRepository().get_all()


@pytest.fixture(scope='function')
def given_a_category_used_by_transaction(client):
    CategoryRepository().save(Category(name='TestCategory', description='Test description'))
    category = CategoryRepository().get_by_name('TestCategory')
    TransactionRepository().save(Transaction(
        transaction_date=datetime.now(),
        amount=Decimal('100'),
        concept='TestConcept',
        category=category
    ))

    return category


def category_exists_on_dashboard(client, category):
    response = client.get('/categories/report')
    assert response.status_code == 200
    assert category.name.encode() in response.data
    assert category.description.encode() in response.data


def category_not_exists_on_dashboard(client, category):
    response = client.get('/categories/report')
    assert response.status_code == 200
    assert category.name.encode() not in response.data
    assert category.description.encode() not in response.data
