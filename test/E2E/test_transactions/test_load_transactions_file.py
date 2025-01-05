import os

from bs4 import BeautifulSoup
from flask import url_for
from werkzeug.datastructures import FileStorage


class TestLoadTransactionsFile:

    def test_load_default_csv_file(self, client):
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_transactions.csv')

        with open(test_file_path, 'rb') as test_file:
            data = {
                'type': 'default',
                'file': (FileStorage(test_file), 'sample_transactions.csv')
            }

            response = client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

        assert response.status_code == 200
        print(response.data.decode('utf-8'))
        assert response.request.path == url_for('transactions_file_blueprint.review_file')
        assert self._response_contains_expected_transactions(response.data) is True

    def _response_contains_expected_transactions(self, response_data: bytes):
        html = BeautifulSoup(response_data, 'html.parser')

        table = html.find('table', {'class': 'table'})
        assert table is not None

        for transaction in self._expected_transactions_data():
            if not self._transaction_exists_in_table(transaction, table):
                return False

        return True

    @staticmethod
    def _transaction_exists_in_table(transaction_data: list[str], html_table):
        rows = html_table.find_all('tr')

        for row in rows:
            cells_text = [cell.text.strip() for cell in row.find_all('td')]
            if all(data in cells_text for data in transaction_data):
                return True

        return False

    @staticmethod
    def _expected_transactions_data() -> list[list[str]]:
        t1 = ["jueves, 25-04-2024", "Adeudo a su cargo pequeneces", "-395"]
        t2 = ["domingo, 21-04-2024", "Www.dazn.com", "-12.99"]
        t3 = ["domingo, 21-04-2024", "Coviran", "-8.38"]
        t4 = ["viernes, 19-04-2024", "Dia", "-5.73"]
        t5 = ["viernes, 19-04-2024", "Adeudo repsol, s.l.u.", "-55.01"]

        return [t1, t2, t3, t4, t5]
