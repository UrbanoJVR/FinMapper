"""
Common helpers for transaction loading tests.
Reusable utilities to make tests more maintainable.
"""
import json
import locale
import os
import re
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from werkzeug.datastructures import FileStorage

from app.src.domain.category import Category
from app.src.domain.file_type import FileType
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TransactionTestHelpers:
    """Helper class for transaction loading tests"""

    @staticmethod
    def load_test_data_from_json(json_filename: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        json_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', json_filename)
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def create_categories_from_data(categories_data: List[Dict[str, str]]):
        """Create categories from test data"""
        cr = CategoryRepository()
        for cat_data in categories_data:
            cr.save(Category(name=cat_data['name'], description=cat_data['description']))

    @staticmethod
    def send_money_manager_file(file_path: str, client) -> Any:
        """Send Money Manager file to the application"""
        with open(file_path, 'rb') as test_file:
            data = {
                'type': FileType.MONEY_MANAGER_APP.name,
                'file': (FileStorage(test_file), 'sample_transactions.xlsx')
            }
            return client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

    @staticmethod
    def send_csv_file(file_path: str, client) -> Any:
        """Send CSV file to the application"""
        with open(file_path, 'rb') as test_file:
            data = {
                'type': FileType.DEFAULT.name,
                'file': (FileStorage(test_file), 'sample_transactions.csv')
            }
            return client.post("/load", data=data, content_type='multipart/form-data', follow_redirects=True)

    @staticmethod
    def format_money_manager_transaction(raw_transaction: Dict[str, str]) -> Dict[str, str]:
        """Format raw Money Manager transaction data to expected format"""
        # Set locale for date formatting
        locale.setlocale(locale.LC_TIME, 'es_ES')
        
        # Format date
        date_str = raw_transaction['raw_date']
        if ' ' in date_str:
            date_dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
        else:
            date_dt = datetime.strptime(date_str, "%d/%m/%Y")
        formatted_date = date_dt.strftime("%A, %d-%m-%Y").lower()
        
        # Clean category (remove emojis)
        category = re.sub(r'[^\w\s]', '', raw_transaction['raw_category']).strip()
        
        # Format amount (negative for expenses)
        amount = f"{-Decimal(raw_transaction['amount']):.2f}"
        
        return {
            'date': formatted_date,
            'category': category,
            'concept': raw_transaction['concept'],
            'amount': amount,
            'comments': raw_transaction['comments']
        }

    @staticmethod
    def assert_all_transactions_present(response_data: bytes, expected_transactions: List[Dict[str, str]]):
        """Assert that all expected transactions are present in the response"""
        html = BeautifulSoup(response_data, 'html.parser')
        table = html.find('table', {'class': 'table'})
        assert table is not None, "No table found in the HTML response!"
        
        missing_transactions = []
        for transaction in expected_transactions:
            if not TransactionTestHelpers._transaction_exists_in_table(transaction, table):
                missing_transactions.append(transaction)
        
        assert not missing_transactions, f"Missing transactions: {missing_transactions}"

    @staticmethod
    def assert_correct_transaction_count(response_data: bytes, expected_count: int):
        """Assert that the correct number of transactions is displayed"""
        html = BeautifulSoup(response_data, 'html.parser')
        table = html.find('table', {'class': 'table'})
        rows = table.find_all('tr')
        actual_count = len(rows) - 1  # Subtract header row
        assert actual_count == expected_count, f"Expected {expected_count} transactions, got {actual_count}"

    @staticmethod
    def _transaction_exists_in_table(transaction: Dict[str, str], html_table) -> bool:
        """Check if a specific transaction exists in the HTML table"""
        rows = html_table.find_all('tr')
        
        for row in rows:
            row_text = row.get_text().lower()
            
            # Check for key identifying fields
            concept_match = transaction['concept'].lower() in row_text
            amount_match = transaction['amount'] in row_text
            
            if concept_match and amount_match:
                return True
        
        return False

    @staticmethod
    def group_transactions_by_month(transactions: List[Dict[str, str]]) -> Dict[tuple, List[Dict[str, str]]]:
        """Group transactions by month and year"""
        grouped = {}
        for transaction in transactions:
            date_str = transaction['date']  # e.g. "martes, 01-07-2025"
            date_dt = datetime.strptime(date_str, "%A, %d-%m-%Y")
            key = (date_dt.month, date_dt.year)
            grouped.setdefault(key, []).append(transaction)
        return grouped

    @staticmethod
    def assert_transactions_in_dashboard(response_data: bytes, expected_transactions: List[Dict[str, str]]):
        """Assert that transactions appear correctly in dashboard"""
        html = BeautifulSoup(response_data, 'html.parser')
        table = html.find('table', {'class': 'table'})
        assert table is not None, "No table found in dashboard response!"
        
        missing_transactions = []
        for transaction in expected_transactions:
            if not TransactionTestHelpers._transaction_exists_in_table(transaction, table):
                missing_transactions.append(transaction)
        
        assert not missing_transactions, f"Missing transactions in dashboard: {missing_transactions}"
