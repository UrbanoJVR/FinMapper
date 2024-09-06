from categories.domain.category import Category
from test_categories.conftest import category_exists_on_dashboard, category_not_exists_on_dashboard


def test_edit_category(client, given_a_category):
    category = given_a_category
    new_category: Category = Category(
        name='another_name',
        description='another_description',
    )

    response = client.post(f"/categories/edit/{category.id}", data={
        'name': new_category.name,
        'description': new_category.description
    }, follow_redirects=True)

    assert response.status_code == 200
    category_not_exists_on_dashboard(client, category)
    category_exists_on_dashboard(client, new_category)
