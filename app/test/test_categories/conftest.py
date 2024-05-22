import pytest

from categories.infraestructure.category_repository import CategoryRepository


@pytest.fixture(scope='function')
def given_a_category(client):
    client.post('/categories/dashboard', data=dict(name='TestCategory', description='Test description'))
    return CategoryRepository().get_by_name('TestCategory')


@pytest.fixture(scope='function')
def given_multiple_categories(client):
    client.post('/categories/dashboard', data=dict(name='Category1', description='Description 1'))
    client.post('/categories/dashboard', data=dict(name='Category2', description='Description 2'))
    client.post('/categories/dashboard', data=dict(name='Category3', description='Description 3'))

    return CategoryRepository().get_all()


def category_exists_on_dashboard(client, category):
    response = client.get('/categories/dashboard')
    assert response.status_code == 200
    assert category.name.encode() in response.data
    assert category.description.encode() in response.data


def category_not_exists_on_dashboard(client, category):
    response = client.get('/categories/dashboard')
    assert response.status_code == 200
    assert category.name.encode() not in response.data
    assert category.description.encode() not in response.data
