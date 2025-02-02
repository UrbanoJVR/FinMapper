import os

from flask import url_for
from werkzeug.datastructures import FileStorage

from app.src.domain.file_type import FileType


class TestLoadTransactionsMoneyManagerAppFile:

    def test_load_transactions_money_manager_app_file(self, client):
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_money_manager_transactions.xlsx')

        with open(test_file_path, 'rb') as test_file:
            data = {
                'type': FileType.MONEY_MANAGER_APP.name,
                'file': (FileStorage(test_file), 'sample_transactions.xlsx')
            }

            review_file_response = client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

        assert review_file_response.status_code == 200
        print(review_file_response.data.decode('utf-8'))
        assert review_file_response.request.path == url_for('transactions_file_blueprint.review_file')

        # assert review_file_response contains exactly data from test file

        # then post to save in memory transactions

        # then review that exactly same transactions are in dashboard