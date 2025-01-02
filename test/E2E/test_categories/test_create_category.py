from app.src.domain.category import Category
from .conftest import category_not_exists_on_dashboard, category_exists_on_dashboard


def test_create_category_when_existing_category(client, given_a_category):
    new_category = Category(name="New Category", description="This is a new category.")
    existing_category = given_a_category
    category_not_exists_on_dashboard(client, new_category)
    category_exists_on_dashboard(client, existing_category)

    response = client.post('/categories/create', data={
        'name': new_category.name,
        'description': new_category.description,
    }, follow_redirects=True)

    assert response.status_code == 200
    category_exists_on_dashboard(client, existing_category)
    category_exists_on_dashboard(client, new_category)
    assert b"Category successfully created!" in response.data


def test_create_category_without_name_is_forbidden(client):
    response = client.post('/categories/create', data={
        'name': None,
        'description': None
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Can&#39;t create category. Invalid data" in response.data
