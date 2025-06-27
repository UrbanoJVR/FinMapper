import locale
import os
import re
from datetime import datetime
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import url_for
from werkzeug.datastructures import FileStorage

from app.src.domain.category import Category
from app.src.domain.file_type import FileType
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestLoadTransactionsMoneyManagerAppFile:

    def test_load_transactions_money_manager_app_file(self, client):
        self._create_categories()
        test_file_path = os.path.join(os.path.dirname(__file__), 'sources', 'test_money_manager_transactions.xlsx')

        review_file_response = self._send_file(test_file_path, client)

        assert review_file_response.status_code == 200
        print(review_file_response.data.decode('utf-8'))
        assert review_file_response.request.path == url_for('transactions_file_blueprint.review_file')

        # TODO refactor with another test to reduce duplicated code
        expected_transactions_data = self._expected_transactions_data()
        missing_transactions = self._missing_transactions_in_response(review_file_response.data,
                                                                      expected_transactions_data)
        assert not missing_transactions, f"Missing transactions in response: {missing_transactions}"
        assert len(expected_transactions_data) == self._count_transactions_in_response(review_file_response.data)

        confirm_response = client.post("/load/review", follow_redirects=True)
        # then navigate to show transactions from specific month/year and check contains expected


        # then review that exactly same transactions are in dashboard

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
            cells_text = [cell.text.strip() for cell in row.find_all('td')]
            if all(data in cells_text for data in transaction_data):
                return True

        return False

    def _expected_transactions_data(self) -> list[list[str]]:
        locale.setlocale(locale.LC_TIME, 'es_ES')

        data = [
            ("31/01/2025 16:29:00", "⛽ Transporte", "Índigo María Molina madrid", "17.99",
             "Parking cañas pre cena autentios"),
            ("31/01/2025 16:27:56", "🪑 Hogar", "Amazon* wk3mq3lw5", "17.99",
             "Baldas transparentes para interior mueble caldera"),
            ("31/01/2025 16:25:15", "🏦 Prestamos", "Cargo por amortización de prestamo/credito", "348.24", ""),
            ("31/01/2025 16:10:10", "🛒 Necesidades básicas", "Recibo wizink", "496.21", "Compras en supermercados"),
            ("30/01/2025 16:24:15", "⚡ Suministros", "Adeudo de endesa", "17.69", "Luz"),
            ("30/01/2025 16:23:29", "⚡ Suministros", "Adeudo digi Spain telecom", "3.00", "Número digi antonio"),
            ("29/01/2025 22:49:27", "🎁 Regalos", "Pastelería raquel", "20.79", "Palmeritas despedida autentia"),
            ("29/01/2025 22:48:43", "⚡ Suministros", "Adeudo orange-france telecom", "85.50", ""),
            ("29/01/2025 16:22:45", "🤱🏻 Cuidado infantil", "Nappy", "81.59", "Pañales y toallitas")
        ]

        formatted_data = []

        for date, category, concept, amount, comments in data:
            # Formating date
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
