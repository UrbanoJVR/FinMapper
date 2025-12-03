from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import url_for

from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.domain.transaction.vo.transaction_type import TransactionType
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class TestMonthlyDashboardWithData:

    def test_monthly_dashboard_shows_category_expenses(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category1 = Category(name="Alimentación", description="Gastos de alimentación")
            category2 = Category(name="Transporte", description="Gastos de transporte")
            category_repository.save(category1)
            category_repository.save(category2)
            
            category1 = category_repository.get_by_name("Alimentación")
            category2 = category_repository.get_by_name("Transporte")
            
            transaction1 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Mercadona",
                type=TransactionType.EXPENSE,
                category=category1
            )
            transaction2 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 20)), 
                amount=TransactionAmount(Decimal("50.00")),
                concept="Gasolina",
                type=TransactionType.EXPENSE,
                category=category2
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)

        response = client.get('/dashboard/2024/1')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        assert "Gastos por Categoría" in response.data.decode('utf-8')
        assert "Alimentación" in response.data.decode('utf-8')
        assert "Transporte" in response.data.decode('utf-8')

    def test_monthly_dashboard_shows_total_expense_amount(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category = Category(name="Alimentación", description="Gastos de alimentación")
            category_repository.save(category)
            
            category = category_repository.get_by_name("Alimentación")
            
            transaction1 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Test 1",
                type=TransactionType.EXPENSE,
                category=category
            )
            transaction2 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 20)), 
                amount=TransactionAmount(Decimal("50.00")),
                concept="Test 2",
                type=TransactionType.EXPENSE,
                category=category
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)

        response = client.get('/dashboard/2024/1')

        assert response.status_code == 200
        assert "150,00 €" in response.data.decode('utf-8')

    def test_monthly_dashboard_collapse_shows_transactions(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category = Category(name="Alimentación", description="Gastos de alimentación")
            category_repository.save(category)
            
            category = category_repository.get_by_name("Alimentación")
            
            transaction = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Mercadona Compra Grande",
                comments="Compra mensual",
                type=TransactionType.EXPENSE,
                category=category
            )
            
            transaction_repository.save(transaction)

        response = client.get('/dashboard/2024/1')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        collapse_divs = html.find_all('div', class_='collapse')
        assert len(collapse_divs) > 0
        
        transactions_found = False
        for collapse in collapse_divs:
            if collapse.find('table', class_='table'):
                transactions_found = True
                break
        
        assert transactions_found, "Should find transactions table in collapse"
        assert "Transacciones" in response.data.decode('utf-8')
        assert "Mercadona Compra Grande" in response.data.decode('utf-8')
        assert "Compra mensual" in response.data.decode('utf-8')

    def test_monthly_dashboard_orders_categories_by_expense_desc(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category1 = Category(name="Alimentación", description="Gastos de alimentación")
            category2 = Category(name="Vivienda", description="Gastos de vivienda")
            category3 = Category(name="Transporte", description="Gastos de transporte")
            category_repository.save(category1)
            category_repository.save(category2)
            category_repository.save(category3)
            
            category1 = category_repository.get_by_name("Alimentación")
            category2 = category_repository.get_by_name("Vivienda")
            category3 = category_repository.get_by_name("Transporte")
            
            transaction1 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Alimentación",
                type=TransactionType.EXPENSE,
                category=category1
            )
            transaction2 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 16)), 
                amount=TransactionAmount(Decimal("500.00")),
                concept="Alquiler",
                type=TransactionType.EXPENSE,
                category=category2
            )
            transaction3 = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 17)), 
                amount=TransactionAmount(Decimal("50.00")),
                concept="Gasolina",
                type=TransactionType.EXPENSE,
                category=category3
            )
            
            transaction_repository.save(transaction1)
            transaction_repository.save(transaction2)
            transaction_repository.save(transaction3)

        response = client.get('/dashboard/2024/1')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        category_names = []
        for item in html.find_all('span', class_='fw-semibold'):
            category_names.append(item.get_text().strip())
        
        assert category_names[0] == "Vivienda"
        assert category_names[1] == "Alimentación"
        assert category_names[2] == "Transporte"

    def test_monthly_dashboard_shows_notes_section(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category = Category(name="Alimentación", description="Gastos de alimentación")
            category_repository.save(category)
            
            category = category_repository.get_by_name("Alimentación")
            
            transaction = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Test",
                type=TransactionType.EXPENSE,
                category=category
            )
            
            transaction_repository.save(transaction)

        response = client.get('/dashboard/2024/1')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        assert "Notas del Mes" in response.data.decode('utf-8')
        
        notes_section = html.find('h5', class_='fw-bold mb-3')
        assert notes_section is not None
        assert 'Notas del Mes' in notes_section.get_text()
        
        collapse_divs = html.find_all('div', class_='collapse')
        notes_in_collapse = False
        for collapse in collapse_divs:
            if 'Notas del Mes' in collapse.get_text():
                notes_in_collapse = True
                break
        assert not notes_in_collapse, "Notes should not be inside a collapse"
        
        textarea = html.find('textarea', class_='form-control')
        assert textarea is not None
        assert "Añade notas sobre los gastos de este mes..." in textarea.get('placeholder', '')
        
        save_button = html.find('button', class_='btn btn-primary mt-3')
        assert save_button is not None
        assert save_button.has_attr('disabled')
        button_text = save_button.get_text()
        assert 'Guardar' in button_text
        assert 'próximamente' in button_text

    def test_monthly_dashboard_has_no_quick_actions(self, client):
        with client.application.app_context():
            category_repository = CategoryRepository()
            transaction_repository = TransactionRepository()
            
            category = Category(name="Alimentación", description="Gastos de alimentación")
            category_repository.save(category)
            
            category = category_repository.get_by_name("Alimentación")
            
            transaction = Transaction(
                transaction_date=TransactionDate(date(2024, 1, 15)), 
                amount=TransactionAmount(Decimal("100.00")),
                concept="Test",
                type=TransactionType.EXPENSE,
                category=category
            )
            
            transaction_repository.save(transaction)

        response = client.get('/dashboard/2024/1')
        html = BeautifulSoup(response.data, 'html.parser')

        assert response.status_code == 200
        
        quick_actions_section = html.find('h3', string=lambda text: text and 'Acciones Rápidas' in text)
        assert quick_actions_section is None, "Should not have Quick Actions section"
        
        quick_action_buttons = html.find_all('a', class_='btn-outline-primary btn-lg')
        quick_action_button_texts = ['Añadir Transacción', 'Ver Movimientos', 'Categorizar', 'Cargar Archivo']
        
        for button_text in quick_action_button_texts:
            found_quick_action_button = False
            for button in quick_action_buttons:
                if button_text in button.get_text() and 'py-4' in button.get('class', []):
                    found_quick_action_button = True
                    break
            assert not found_quick_action_button, f"Should not have {button_text} quick action button"
