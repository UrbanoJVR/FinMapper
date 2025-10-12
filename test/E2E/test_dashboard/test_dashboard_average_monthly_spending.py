from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestDashboardAverageMonthlySpending:

    def test_given_no_transactions_when_access_dashboard_then_redirect_to_empty(self, client):
        # Act - Access dashboard for 2024 with no transactions (should redirect to empty dashboard)
        response = client.get('/dashboard/2024', follow_redirects=True)

        # Assert - Check response
        assert response.status_code == 200
        assert "No hay datos para este año" in response.data.decode('utf-8'), "Should show empty dashboard message"

    def test_given_transactions_in_two_months_then_show_correct_average(self, client):
        # Arrange - Create transactions in 2 months (January: 100, June: 200)
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("100.00"), 
                concept="January transaction"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 6, 20), 
                amount=Decimal("200.00"), 
                concept="June transaction"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Find all cards
        cards = html.find_all('div', class_='card')
        assert len(cards) >= 2, "Should have at least 2 cards"
        
        # Find the average monthly spending card (second card)
        avg_card = cards[1]
        card_title = avg_card.find('h6', class_='card-title')
        assert card_title is not None, "Average card title should be present"
        assert "Gasto Medio Mensual" in card_title.text, f"Expected 'Gasto Medio Mensual' in title, got: {card_title.text}"
        
        # Check the card value (should be 150.00 = (100 + 200) / 2)
        card_value = avg_card.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "150.00 €" in card_value.text, f"Expected '150.00 €' in value, got: {card_value.text}"

    def test_given_transactions_in_three_distinct_months_then_show_correct_average(self, client):
        # Arrange - Create transactions in 3 distinct months
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("300.00"), 
                concept="January transaction"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 5, 20), 
                amount=Decimal("600.00"), 
                concept="May transaction"
            )
            transaction3 = Transaction(
                transaction_date=date(2024, 12, 10), 
                amount=Decimal("900.00"), 
                concept="December transaction"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)
            transaction_repository.save(transaction3)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Find all cards
        cards = html.find_all('div', class_='card')
        avg_card = cards[1]
        
        # Check the card value (should be 600.00 = (300 + 600 + 900) / 3)
        card_value = avg_card.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "600.00 €" in card_value.text, f"Expected '600.00 €' in value, got: {card_value.text}"

    def test_given_all_transactions_in_same_month_then_average_equals_total(self, client):
        # Arrange - Create multiple transactions in the same month
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 3, 1), 
                amount=Decimal("100.00"), 
                concept="Transaction 1"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 3, 15), 
                amount=Decimal("200.00"), 
                concept="Transaction 2"
            )
            transaction3 = Transaction(
                transaction_date=date(2024, 3, 30), 
                amount=Decimal("150.00"), 
                concept="Transaction 3"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)
            transaction_repository.save(transaction3)

        # Act - Access dashboard for 2024
        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        # Assert - Check response and content
        assert response.status_code == 200
        
        # Find all cards
        cards = html.find_all('div', class_='card')
        
        # Check total expenses card (first card)
        total_card = cards[0]
        total_value = total_card.find('h3', class_='card-text')
        assert "450.00 €" in total_value.text, f"Expected '450.00 €' in total, got: {total_value.text}"
        
        # Check average card (second card) - should equal total since only 1 month
        avg_card = cards[1]
        avg_value = avg_card.find('h3', class_='card-text')
        assert "450.00 €" in avg_value.text, f"Expected '450.00 €' in average, got: {avg_value.text}"

    def test_given_mixed_positive_negative_amounts_then_show_correct_average(self, client):
        # Arrange - Create transactions with mixed amounts in 2 months
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("500.00"), 
                concept="Income"
            )
            transaction2 = Transaction(
                transaction_date=date(2024, 1, 20), 
                amount=Decimal("-100.00"), 
                concept="Expense"
            )
            transaction3 = Transaction(
                transaction_date=date(2024, 6, 10), 
                amount=Decimal("-200.00"), 
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
        
        # Find all cards
        cards = html.find_all('div', class_='card')
        avg_card = cards[1]
        
        # Check the card value (should be 100.00 = (500 - 100 - 200) / 2)
        card_value = avg_card.find('h3', class_='card-text')
        assert card_value is not None, "Card value should be present"
        assert "100.00 €" in card_value.text, f"Expected '100.00 €' in value, got: {card_value.text}"

