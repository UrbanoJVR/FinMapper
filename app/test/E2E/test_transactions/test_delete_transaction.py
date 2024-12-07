from .conftest import transaction_exists, transaction_not_exists, count_transactions_in_table


class TestDeleteTransaction:

    def test_delete_transaction_and_redirect_to_transactions_table(self, client, given_a_transaction):
        transaction_to_be_deleted = given_a_transaction
        origin_url = f"/movements/{transaction_to_be_deleted.transaction_date.month}/{transaction_to_be_deleted.transaction_date.year}"

        assert transaction_exists(client, transaction_to_be_deleted)
        transactions_count_before_delete = count_transactions_in_table(client,
                                                                       transaction_to_be_deleted.transaction_date.month,
                                                                       transaction_to_be_deleted.transaction_date.year)

        response = client.get(f"/transactions/delete/{transaction_to_be_deleted.id}",
                              follow_redirects=True,
                              headers={"Referer": origin_url})
        transactions_count_after_delete = count_transactions_in_table(client,
                                                                      transaction_to_be_deleted.transaction_date.month,
                                                                      transaction_to_be_deleted.transaction_date.year)

        assert response.status_code == 200
        assert response.request.path == origin_url
        assert b'<table class="table table-striped table-hover mt-4">' in response.data
        assert '<option selected value="12">Diciembre</option>'.encode('utf-8') in response.data
        assert transaction_not_exists(client, transaction_to_be_deleted)
        assert transactions_count_before_delete - transactions_count_after_delete == 1
