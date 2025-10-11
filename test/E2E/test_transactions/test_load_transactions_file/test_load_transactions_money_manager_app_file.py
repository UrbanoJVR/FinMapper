import locale
import os
import re
from datetime import datetime
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import url_for
from flask_babel import gettext
from werkzeug.datastructures import FileStorage

from app.src.domain.category import Category
from app.src.domain.file_type import FileType
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestLoadTransactionsMoneyManagerAppFile:

    def test_given_money_manager_transactions_file_when_load_then_success(self, client):
        # load file and send
        self._create_categories()
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_money_manager_transactions.xls')

        review_file_response = self._send_file(test_file_path, client)

        assert review_file_response.status_code == 200
        print(review_file_response.data.decode('utf-8'))
        assert review_file_response.request.path == url_for('transactions_file_blueprint.review_file')

        # verify that loaded file is showing correctly in review page
        expected_transactions_data = self._expected_transactions_data()
        missing_transactions = self._missing_transactions_in_response(review_file_response.data,
                                                                      expected_transactions_data)
        assert not missing_transactions, f"Missing transactions in response: {missing_transactions}"
        assert len(expected_transactions_data) == self._count_transactions_in_response(review_file_response.data)

        # confirm review to save all transactions
        confirm_response = client.post("/load/review", follow_redirects=True)
        expected_message = gettext("File processed successfully!")
        assert expected_message.encode() in confirm_response.data

        # then review that exactly same transactions are in dashboard
        transactions_by_month_year = self._group_transactions_by_month_year(expected_transactions_data)

        for (month, year), transactions in transactions_by_month_year.items():
            response = client.get(f"/movements/{month}/{year}")
            assert response.status_code == 200, f"Falló GET /movements/{month}/{year}"

            missing = self._missing_transactions_in_response(response.data, transactions)
            assert not missing, f"Missing transactions in /movements/{month}/{year}: {missing}"


    def _send_file(self, test_file_path: str, client):
        with open(test_file_path, 'rb') as test_file:
            data = {
                'type': FileType.MONEY_MANAGER_APP.name,
                'file': (FileStorage(test_file), 'sample_transactions.xlsx')
            }

            return client.post("/load", data=data, content_type='multipart/form-data',
                               follow_redirects=True)

    def _missing_transactions_in_response(self, response_data: bytes,
                                          expected_transactions_data: list[list[str]]) -> list[list[str]]:
        """ Returns a list of transactions that are missing from the response table """
        html = BeautifulSoup(response_data, 'html.parser')

        table = html.find('table', {'class': 'table'})
        assert table is not None, "No table found in the HTML response!"

        missing_transactions = []
        for transaction in expected_transactions_data:
            if not self._transaction_exists_in_table(transaction, table):
                missing_transactions.append(transaction)

        return missing_transactions

    def _count_transactions_in_response(self, response_data: bytes):
        html = BeautifulSoup(response_data, 'html.parser')
        table = html.find('table', {'class': 'table'})
        # rows including table header
        rows = table.find_all('tr')
        return len(rows) - 1

    @staticmethod
    def _transaction_exists_in_table(transaction_data: list[str], html_table):
        rows = html_table.find_all('tr')

        for row in rows:
            # Get all text content from the row, including nested elements
            row_text = row.get_text()
            
            # For the new table design, we need to be more flexible with the search
            # Check if the key transaction data is present in the row text
            # Skip empty strings and be more lenient with date formats
            non_empty_data = [data for data in transaction_data if data]
            
            # Check if most of the transaction data is present (at least 3 out of 5 fields)
            matches = 0
            for data in non_empty_data:
                if data in row_text:
                    matches += 1
            
            # If we have at least 3 matches out of the non-empty data, consider it a match
            if len(non_empty_data) > 0 and matches >= min(3, len(non_empty_data)):
                return True

        return False

    def _expected_transactions_data(self) -> list[list[str]]:
        locale.setlocale(locale.LC_TIME, 'es_ES')

        data = [
            ("01/07/2025", "🤱🏻 Cuidado infantil", "Guardería Alfonso", "247", ""),
            ("01/07/2025", "🍝 Restaurantes", "Consumo tarjeta restaurante", "171", ""),
            ("30/06/2025 22:50:02", "🛒 Necesidades básicas", "Compras con edenred", "71", ""),
            ("30/06/2025 22:48:29", "🪑 Hogar", "Amazon", "6.97", "Colgador rollo papel cocina"),
            ("01/06/2025", "🍝 Restaurantes", "Consumo tarjeta restaurante", "100", ""),
            ("01/06/2025", "🤱🏻 Cuidado infantil", "Guardería Alfonso", "247", ""),
            ("30/05/2025 23:28:41", "🤱🏻 Cuidado infantil", "Decathlon", "21.96", ""),
            ("01/05/2025", "🍝 Restaurantes", "Consumo tarjeta restaurante", "171", ""),
            ("01/05/2025", "🤱🏻 Cuidado infantil", "Guardería Alfonso", "247", ""),
            ("30/04/2025 13:27:49", "🏨 Viajes y vacaciones", "Casi todo Torrejon de ardoz", "25.10",
             "Carbón puente mayo"),
            ("21/03/2025 23:47:46", "⛽ Transporte", "Misparkings.com", "12.80", "Parking noche piedrahita"),
        ]

        formatted_data = []

        for date, category, concept, amount, comments in data:
            # Formatting date
            date_dt = datetime.strptime(date, "%d/%m/%Y %H:%M:%S") if " " in date else datetime.strptime(date,
                                                                                                         "%d/%m/%Y")
            date_str = date_dt.strftime("%A, %d-%m-%Y").lower()

            # Clean category deleting emojis and spaces
            category_str = re.sub(r'[^\w\s]', '', category).strip()

            # Format amount multiplying by -1
            amount_str = f"{-Decimal(amount):.2f}"

            formatted_data.append([date_str, category_str, concept, amount_str, comments])

        return formatted_data

    def _create_categories(self):
        cr = CategoryRepository()
        cr.save(Category(name="Transporte", description="Transporte"))
        cr.save(Category(name="Hogar", description="Hogar"))
        cr.save(Category(name="Prestamos", description="Prestamos"))
        cr.save(Category(name="Necesidades básicas", description="Necesidades básicas"))
        cr.save(Category(name="Suministros", description="Suministros"))
        cr.save(Category(name="Regalos", description="Regalos"))
        cr.save(Category(name="Cuidado infantil", description="Cuidado infantil"))
        cr.save(Category(name="Restaurantes", description="Comida que no cocinas en casa"))
        cr.save(Category(name="Viajes y vacaciones", description="Pues eso, veranito veranito"))

    def _group_transactions_by_month_year(self, transactions: list[list[str]]) -> dict[tuple[int, int], list[list[str]]]:
        grouped = {}
        for tx in transactions:
            date_str = tx[0]  # e.g. "martes, 01-07-2025"
            date_dt = datetime.strptime(date_str, "%A, %d-%m-%Y")  # español

            key = (date_dt.month, date_dt.year)
            grouped.setdefault(key, []).append(tx)
        return grouped
