def test_example(client):
    response = client.get('/dashboard')
    assert response.status_code == 200


# def test_categories_list(client):
#     response = client.get('/categories/dashboard')
#     assert response.status_code == 200


# def test_create_category(client):
#     response = client.post('/categories/', data=dict(name='test', description='test'))
#     assert response.status_code == 200
