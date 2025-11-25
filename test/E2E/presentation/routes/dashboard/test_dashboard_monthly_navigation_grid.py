from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestDashboardMonthlyNavigationGrid:

    def test_dashboard_shows_monthly_navigation_grid_with_active_months(self, client):
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction1 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=Decimal("100.00"), 
                concept="January transaction"
            )
            transaction2 = Transaction(
                transaction_date=TransactionDate(date(2024, 6, 20)), 
                amount=Decimal("200.00"), 
                concept="June transaction"
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)

        response = client.get('/dashboard/2024')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        january_link = html.find('a', href='/dashboard/2024/1')
        assert january_link is not None
        assert 'btn-outline-primary' in january_link.get('class', [])
        
        june_link = html.find('a', href='/dashboard/2024/6')
        assert june_link is not None
        assert 'btn-outline-primary' in june_link.get('class', [])
        
        disabled_buttons = html.find_all('button', disabled=True)
        assert len(disabled_buttons) >= 10
        
        for button in disabled_buttons:
            assert 'btn-outline-secondary' in button.get('class', [])

    def test_monthly_navigation_uses_correct_year_in_urls(self, client):
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction = Transaction(
                transaction_date=TransactionDate(date(2023, 3, 15)), 
                amount=Decimal("100.00"), 
                concept="March 2023 transaction"
            )
            
            transaction_repository.save(transaction)

        response = client.get('/dashboard/2023')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        march_link = html.find('a', href='/dashboard/2023/3')
        assert march_link is not None
        assert 'btn-outline-primary' in march_link.get('class', [])

    def test_dashboard_without_data_shows_no_monthly_grid(self, client):
        response = client.get('/dashboard/2024', follow_redirects=True)

        assert response.status_code == 200
        assert "No hay datos para este año" in response.data.decode('utf-8')
