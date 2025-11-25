from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import url_for

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from .conftest import transaction_exists


class TestCreateTransaction:

    def test_create_transaction_and_clean_screen(self, client):
        transaction_to_create = Transaction(
            amount=Decimal(20.50),
            concept='Transaction concept',
            transaction_date=TransactionDate(date(2024, 12, 1)),
            comments='Transaction comments'
        )

        response = client.post('/transactions/add',
                               data=dict(amount=transaction_to_create.amount, concept=transaction_to_create.concept,
                                         comments=transaction_to_create.comments,
                                         date=transaction_to_create.transaction_date.value.strftime('%Y-%m-%d')),
                               follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == url_for('transactions_crud_blueprint.create_transaction')
        self._assert_form_is_empty(response)
        assert transaction_exists(client, transaction_to_create)

    @staticmethod
    def _assert_form_is_empty(response):
        html = BeautifulSoup(response.data, 'html.parser')
        form = html.find('form', attrs={'class': 'form'})
        assert form is not None, "Form not found"

        # Check the date field
        date_field = form.find('input', {'name': 'date'})
        today = date.today().strftime('%Y-%m-%d')
        assert date_field is not None, "Date field not found"
        assert date_field['value'] == today, f"Date field should be {today}"

        # Check that the amount field is empty
        amount_field = form.find('input', {'name': 'amount'})
        assert amount_field is not None, "Amount field not found"
        assert amount_field['value'] == '', "Amount field is not empty"

        # Check that the concept field is empty
        concept_field = form.find('input', {'name': 'concept'})
        assert concept_field is not None, "Concept field not found"
        assert concept_field['value'] == '', "Concept field is not empty"

        # Check that the category field is empty
        category_field = form.find('select', {'name': 'category_id'})
        assert category_field is not None, "Category field not found"
        selected_option = category_field.find('option', {'selected': True})
        assert selected_option is None or selected_option['value'] == 'None', "Category field is not empty"

        # Check that the comments field is empty
        comments_field = form.find('input', {'name': 'comments'})
        assert comments_field is not None, "Comments field not found"
        assert comments_field['value'] == '', "Comments field is not empty"
