import pytest


@pytest.fixture(scope='function')
def given_a_category(client):
    client.post('/categories/dashboard', data=dict(name='TestCategory', description='Test description'))
