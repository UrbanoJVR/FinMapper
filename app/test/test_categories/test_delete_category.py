# Given a category should delete it with success message
# Given a test_categories list should delte one category with success message and still showing not delted test_categories
# Given a transaction with category should can not delete the category and show message
from flask import url_for

from test_categories.conftest import category_exists_on_dashboard, category_not_exists_on_dashboard


def test_delete_category(client, given_multiple_categories):
    categories = given_multiple_categories
    for category in categories:
        category_exists_on_dashboard(client, category)

    response = client.get(f"/categories/delete/{categories[1].id}", follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for('categories_blueprint.categories_dashboard')
    assert b'Category successfully deleted!' in response.data

    category_exists_on_dashboard(client, categories[0])
    category_not_exists_on_dashboard(client, categories[1])
    category_exists_on_dashboard(client, categories[2])


def test_delete_forbidden_when_category_is_used(client, given_a_category_used_by_transaction):
    category = given_a_category_used_by_transaction
    category_exists_on_dashboard(client, category)

    response = client.get(f"/categories/delete/{category.id}", follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for('categories_blueprint.categories_dashboard')
    assert b'Can&#39;t delete used category!' in response.data
    category_exists_on_dashboard(client, category)
