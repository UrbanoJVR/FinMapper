import os
from bs4 import BeautifulSoup
from flask import url_for
from werkzeug.datastructures import FileStorage

from app.src.domain.file_type import FileType


class TestLoadTransactionsCsvDefaultFile:

    def test_load_default_csv_file(self, client):
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_transactions_default.csv')

        with open(test_file_path, 'rb') as test_file:
            data = {
                'type': FileType.DEFAULT.name,
                'file': (FileStorage(test_file), 'sample_transactions.csv')
            }

            response = client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        print(response.data.decode('utf-8'))

        assert response.request.path == url_for('transactions_file_blueprint.review_file')

        missing_transactions = self._missing_transactions_in_response(response.data)
        assert not missing_transactions, f"Missing transactions in response: {missing_transactions}"

    def _missing_transactions_in_response(self, response_data: bytes):
        """ Returns a list of transactions that are missing from the response table """
        html = BeautifulSoup(response_data, 'html.parser')

        table = html.find('table', {'class': 'table'})
        assert table is not None, "No table found in the HTML response!"

        missing_transactions = []
        for transaction in self._expected_transactions_data():
            if not self._transaction_exists_in_table(transaction, table):
                missing_transactions.append(transaction)

        return missing_transactions

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
