from categories.domain.category import Category


def test_create_first_category(client):
    category = Category(name="New Category", description="This is a new category.")
    response = client.post('/categories/dashboard', data={
        'name': category.name,
        'description': category.description,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Category successfully created!" in response.data
    assert category.name.encode() in response.data
    assert category.description.encode() in response.data
    assert b"TestCategory" not in response.data
    assert b"Test description" not in response.data


def test_get_categories_when_existing_category(client, given_a_category):
    response = client.post('/categories/dashboard', data={
        'name': 'New Category',
        'description': 'This is a new category.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"TestCategory" in response.data
    assert b"Test description" in response.data
    assert b"Category successfully created!" in response.data
    assert b"New Category" in response.data
    assert b"This is a new category" in response.data


def test_create_category_without_name_is_forbidden(client):
    response = client.post('/categories/dashboard', data={
        'name': None,
        'description': None
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Can&#39;t create category" in response.data
