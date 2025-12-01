import os
from flask import url_for
from flask_babel import gettext

from .helpers.transaction_test_helpers import TransactionTestHelpers


class TestLoadTransactionsMoneyManagerAppFile:

    def test_load_money_manager_file_successfully(self, client):
        """Test that Money Manager file loads without errors"""
        # Given
        self._setup_test_data()
        test_file_path = self._get_test_file_path()
        
        # When
        response = TransactionTestHelpers.send_money_manager_file(test_file_path, client)
        
        # Then
        assert response.status_code == 200
        assert response.request.path == url_for('transactions_file_blueprint.review_file')

    def test_review_page_shows_expected_transactions(self, client):
        """Test that review page displays all expected transactions"""
        # Given
        self._setup_test_data()
        test_file_path = self._get_test_file_path()
        expected_transactions = self._get_expected_transactions()
        
        # When
        response = TransactionTestHelpers.send_money_manager_file(test_file_path, client)
        
        # Then
        TransactionTestHelpers.assert_all_transactions_present(response.data, expected_transactions)
        TransactionTestHelpers.assert_correct_transaction_count(response.data, len(expected_transactions))

    def test_confirm_saves_transactions_successfully(self, client):
        """Test that confirming the review saves transactions to database"""
        # Given
        self._setup_test_data()
        test_file_path = self._get_test_file_path()
        TransactionTestHelpers.send_money_manager_file(test_file_path, client)
        
        # When
        confirm_response = client.post("/load/review", follow_redirects=True)
        
        # Then
        expected_message = gettext("File processed successfully!")
        assert expected_message.encode() in confirm_response.data

    def test_transactions_appear_in_dashboard_by_month(self, client):
        """Test that saved transactions appear correctly in dashboard by month"""
        # Given
        self._setup_test_data()
        test_file_path = self._get_test_file_path()
        expected_transactions = self._get_expected_transactions()
        
        # Load and confirm transactions
        TransactionTestHelpers.send_money_manager_file(test_file_path, client)
        client.post("/load/review", follow_redirects=True)
        
        # When & Then
        transactions_by_month = TransactionTestHelpers.group_transactions_by_month(expected_transactions)
        for (month, year), transactions in transactions_by_month.items():
            response = client.get(f"/movements/{month}/{year}")
            assert response.status_code == 200, f"Failed to load movements for {month}/{year}"
            TransactionTestHelpers.assert_transactions_in_dashboard(response.data, transactions)

    # Private helper methods

    def _setup_test_data(self):
        """Setup test data from JSON file"""
        test_data = TransactionTestHelpers.load_test_data_from_json('money_manager_transactions.json')
        TransactionTestHelpers.create_categories_from_data(test_data['categories'])

    def _get_test_file_path(self):
        """Get path to test file"""
        return os.path.join(os.path.dirname(__file__), 'sources', 'test_money_manager_transactions.xls')

    def _get_expected_transactions(self):
        """Get expected transaction data from JSON and format it"""
        test_data = TransactionTestHelpers.load_test_data_from_json('money_manager_transactions.json')
        return [TransactionTestHelpers.format_money_manager_transaction(tx) for tx in test_data['transactions']]
