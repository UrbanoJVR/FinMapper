import os

from flask import url_for
from werkzeug.datastructures import FileStorage

from app.src.domain.file_type import FileType


class TestLoadTransactionsMoneyManagerAppFile:

    def test_load_transactions_money_manager_app_file(self, client):
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_transactions_default.csv')

        with open(test_file_path, 'rb') as test_file:
            data = {
                'type': FileType.MONEY_MANAGER_APP.name,
                'file': (FileStorage(test_file), 'sample_transactions.xlsx')
            }

            response = client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

        assert response.status_code == 200
        print(response.data.decode('utf-8'))
        assert response.request.path == url_for('transactions_file_blueprint.review_file')