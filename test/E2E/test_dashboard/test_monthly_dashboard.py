import pytest
from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestMonthlyDashboard:

    def test_given_no_transactions_when_access_monthly_dashboard_then_redirect_to_empty(self, client):
        response = client.get('/dashboard/2024/1', follow_redirects=True)

        assert response.status_code == 200
        assert "No hay datos para este mes" in response.data.decode('utf-8'), "Should show empty monthly dashboard message"
        assert "Hola Enero" in response.data.decode('utf-8'), "Should show month name in Spanish"

    def test_given_transactions_in_month_then_show_monthly_dashboard(self, client):
        with client.application.app_context():
            transaction_repository = TransactionRepository()
            
            transaction = Transaction(
                transaction_date=date(2024, 1, 15), 
                amount=Decimal("100.00"), 
                concept="January transaction"
            )
            
            transaction_repository.save(transaction)

        response = client.get('/dashboard/2024/1')

        assert response.status_code == 200
        assert "Hola Enero" in response.data.decode('utf-8'), "Should show month name in Spanish"
        assert "Dashboard mensual en desarrollo" in response.data.decode('utf-8'), "Should show development message"

    def test_monthly_dashboard_navigation_previous_month(self, client):
        response = client.get('/dashboard/2024/2', follow_redirects=True)
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        # Find the "Mes anterior" button
        previous_button = html.find('a', href='/dashboard/2024/1')
        assert previous_button is not None, "Previous month button should be present"
        assert 'Mes anterior' in previous_button.get_text(), "Previous button should contain 'Mes anterior' text"

    def test_monthly_dashboard_navigation_next_month(self, client):
        response = client.get('/dashboard/2024/2', follow_redirects=True)
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        # Find the "Mes siguiente" button
        next_button = html.find('a', href='/dashboard/2024/3')
        assert next_button is not None, "Next month button should be present"
        assert 'Mes siguiente' in next_button.get_text(), "Next button should contain 'Mes siguiente' text"

    def test_monthly_dashboard_navigation_from_january_to_previous_december(self, client):
        response = client.get('/dashboard/2024/1', follow_redirects=True)
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        # Find the "Mes anterior" button
        previous_button = html.find('a', href='/dashboard/2023/12')
        assert previous_button is not None, "Previous month button should be present"
        assert 'Mes anterior' in previous_button.get_text(), "Previous button should contain 'Mes anterior' text"

    def test_monthly_dashboard_navigation_from_december_to_next_january(self, client):
        response = client.get('/dashboard/2024/12', follow_redirects=True)
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        # Find the "Mes siguiente" button
        next_button = html.find('a', href='/dashboard/2025/1')
        assert next_button is not None, "Next month button should be present"
        assert 'Mes siguiente' in next_button.get_text(), "Next button should contain 'Mes siguiente' text"

    def test_invalid_month_redirects_to_yearly_dashboard(self, client):
        response = client.get('/dashboard/2024/13', follow_redirects=True)

        # Should redirect to yearly dashboard
        assert response.status_code == 200
        assert "Resumen financiero del año" in response.data.decode('utf-8'), "Should redirect to yearly dashboard"

    @pytest.mark.parametrize("month,expected_spanish_name", [
        (1, "Enero"),
        (6, "Junio"),
        (12, "Diciembre")
    ])
    def test_month_names_are_in_spanish(self, client, month, expected_spanish_name):
        response = client.get(f'/dashboard/2024/{month}', follow_redirects=True)

        assert response.status_code == 200
        assert f"Hola {expected_spanish_name}" in response.data.decode('utf-8'), f"Should show 'Hola {expected_spanish_name}'"

    def test_empty_monthly_dashboard_shows_quick_actions(self, client):
        response = client.get('/dashboard/2024/1', follow_redirects=True)

        assert response.status_code == 200
        assert "Acciones Rápidas" in response.data.decode('utf-8'), "Should show quick actions section"
        assert "Añadir Transacción" in response.data.decode('utf-8'), "Should show add transaction button"
        assert "Ver Movimientos" in response.data.decode('utf-8'), "Should show view movements button"
