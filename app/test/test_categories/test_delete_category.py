# Given a category should delete it with success message
# Given a test_categories list should delte one category with success message and still showing not delted test_categories
# Given a transaction with category should can not delete the category and show message
from flask import url_for

from test_categories.conftest import category_exists_on_dashboard


def test_delete_category(client, given_a_category):
    category = given_a_category
    category_exists_on_dashboard(client, category)
    # response = client.get('/test_categories/dashboard/{}'.format(category.id))

    response = client.get('/categories/delete/' + str(category.id), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for('categories_blueprint.categories_dashboard')
    assert b'Category successfully deleted!' in response.data
    assert category.name.encode() not in response.data
    assert category.description.encode() not in response.data


def test_delete_forbidden_when_category_is_used(client, given_a_category):
    pass
