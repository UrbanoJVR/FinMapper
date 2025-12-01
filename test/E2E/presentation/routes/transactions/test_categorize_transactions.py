from bs4 import BeautifulSoup

from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from test.unit.domain.category.mother.category_mother import CategoryMother
from test.unit.domain.transaction.mother.transaction_mother import TransactionMother


class TestCategorizeTransactions:

    def test_categorize_transactions_when_no_uncategorized_transactions_should_load_successfully(self, client):
        # Crear una categoría para que el formulario tenga opciones
        category = CategoryMother().random()
        CategoryRepository().save(category)

        # Acceder a la ruta de categorización cuando no hay transacciones sin categorizar
        response = client.get('/transactions/categorize', follow_redirects=True)

        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')

        # Verificar que la página carga correctamente
        # Debería mostrar el título y la tabla (aunque esté vacía)
        title = soup.find('h4', class_='fw-bold')
        assert title is not None, "Title should be present"

        # Verificar que existe la tabla
        table = soup.find('table', class_='table')
        assert table is not None, "Table should be present"

        # Verificar que el formulario existe
        form = soup.find('form', id='categorize-form')
        assert form is not None, "Form should be present"

        # Verificar que no hay filas de transacciones (solo el header)
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            assert len(rows) == 0, "Should have no transaction rows when there are no uncategorized transactions"

    def test_categorize_transactions_when_all_transactions_are_categorized_should_load_successfully(self, client):
        # Crear una categoría
        category = CategoryMother().random()
        CategoryRepository().save(category)

        # Crear una transacción ya categorizada
        transaction = TransactionMother().random()
        transaction = transaction.to_builder().category(category).build()
        TransactionRepository().save(transaction)

        # Acceder a la ruta de categorización
        response = client.get('/transactions/categorize', follow_redirects=True)

        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')

        # Verificar que la página carga correctamente
        title = soup.find('h4', class_='fw-bold')
        assert title is not None, "Title should be present"

        # Verificar que existe la tabla
        table = soup.find('table', class_='table')
        assert table is not None, "Table should be present"

        # Verificar que no hay filas de transacciones sin categorizar
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            assert len(rows) == 0, "Should have no transaction rows when all transactions are categorized"
