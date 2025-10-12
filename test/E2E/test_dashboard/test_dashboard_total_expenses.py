from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestDashboardTotalExpenses:

    def test_given_no_transactions_when_access_dashboard_then_show_zero_total(self, client):
        # Act - Access dashboard for 2024 with no transactions (should redirect to empty dashboard)
        response = client.get('/dashboard/2024', follow_redirects=True)
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Check that we're redirected to empty dashboard and it shows the appropriate message
        assert "No hay datos para este año" in response.data.decode('utf-8'), "Should show empty dashboard message"
        
        # Check that quick actions are present
        assert "Acciones Rápidas" in response.data.decode('utf-8'), "Should show quick actions"

    def test_given_transactions_when_access_dashboard_then_show_correct_total_sum(self, client):
        # Arrange - Create transactions directly in the test client's database
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            # Create transactions for 2024
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("100.50"), 
                concept="Test transaction 1"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 6, 20), 
                amount=Decimal("200.25"), 
                concept="Test transaction 2"
            )
            transaction3 = Transaction(
                transaction_date=date(2023, 12, 31),  # Different year - should not be included
                amount=Decimal("300.00"), 
                concept="Test transaction 3"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)
            transaction_repository.save(transaction3)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Check that the total expenses card is present
        total_expenses_card = html.find('div', class_='card')
        assert total_expenses_card is not None, "Total expenses card should be present"
        
        # Check the card title
        card_title = total_expenses_card.find('h6', class_='card-title')
        assert card_title is not None, "Card title should be present"
        assert "Total Gastos 2024" in card_title.text, f"Expected 'Total Gastos 2024' in title, got: {card_title.text}"
        
        # Check the card value (should be 300.75 = 100.50 + 200.25)
        card_value = total_expenses_card.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "300.75 €" in card_value.text, f"Expected '300.75 €' in value, got: {card_value.text}"

    def test_given_negative_transactions_when_access_dashboard_then_show_correct_total(self, client):
        # Arrange - Create transactions with negative amounts
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("-100.00"), 
                concept="Expense 1"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 6, 20), 
                amount=Decimal("-50.50"), 
                concept="Expense 2"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Check the card value (should be -150.50)
        card_value = html.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "-150.50 €" in card_value.text, f"Expected '-150.50 €' in value, got: {card_value.text}"

    def test_given_mixed_transactions_when_access_dashboard_then_show_correct_total(self, client):
        # Arrange - Create transactions with mixed positive and negative amounts
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("200.00"), 
                concept="Income"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 6, 20), 
                amount=Decimal("-75.25"), 
                concept="Expense"
            )
            transaction3 = Transaction(
                transaction_date=date(2024, 12, 1), 
                amount=Decimal("-25.00"), 
                concept="Expense"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)
            transaction_repository.save(transaction3)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Check the card value (should be 99.75 = 200.00 - 75.25 - 25.00)
        card_value = html.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "99.75 €" in card_value.text, f"Expected '99.75 €' in value, got: {card_value.text}"
