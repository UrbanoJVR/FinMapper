from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import url_for

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.repository.category_repository import CategoryRepository
from test.conftest import assert_flash_message_success_is_present

class TestEditTransaction:

    def test_edit_transaction(self, client, given_a_transaction):
        existing_transaction = given_a_transaction
        new_transaction = Transaction(
            amount=TransactionAmount(Decimal(999.00)),
            concept="New concept",
            comments="New comments",
            transaction_date=TransactionDate(date.min),
            category=None,
            id=existing_transaction.id,
        )
        edit_transaction_url = f"/edit-transaction/{existing_transaction.id}"
        # assert existing category is in table
        self._assert_edit_form_contains_transaction_data(client, existing_transaction)

        # send new data to edit existing transaction
        result_after_edit = client.post(edit_transaction_url,
                                        data=dict(amount=new_transaction.amount.value,
                                                  concept=new_transaction.concept,
                                                  comments=new_transaction.comments,
                                                  date=new_transaction.transaction_date.value.strftime('%Y-%m-%d'))
                                        , follow_redirects=True)
        assert result_after_edit.status_code == 200
        # assert reload works
        assert result_after_edit.request.path == url_for('transactions_crud_blueprint.movements_list',
                                                         month=new_transaction.transaction_date.value.month,
                                                         year=new_transaction.transaction_date.value.year)
        # assert transaction exists with new data
        self._assert_edit_form_contains_transaction_data(client, new_transaction)
        # assert success message is visible
        assert_flash_message_success_is_present(result_after_edit.data, "Transacción actualizada exitosamente")

    def _assert_edit_form_contains_transaction_data(self, client, transaction):
        response = client.get(f"/edit-transaction/{transaction.id}")
        assert response.status_code == 200

        html = BeautifulSoup(response.data, 'html.parser')
        form = html.find('form', attrs={'class': 'form'})
        assert form is not None, "Form not found"

        # Check the date field
        date_field = form.find('input', {'name': 'date'})
        date = transaction.transaction_date.value.strftime('%Y-%m-%d')
        assert date_field is not None, "Date field not found"
        assert date_field['value'] == date, f"Date field should be {date} (same as expected transaction)"

        # Check amount field
        amount_field = form.find('input', {'name': 'amount'})
        assert amount_field is not None, "Amount field not found"
        actual_value: Decimal = Decimal(amount_field['value'])
        assert actual_value == transaction.amount.value, "Amount field is not the same than transaction"

        # Check concept field
        concept_field = form.find('input', {'name': 'concept'})
        assert concept_field is not None, "Concept field not found"
        assert concept_field['value'] == transaction.concept, "Concept field is the same than transaction"

        # Check comments field
        comments_field = form.find('input', {'name': 'comments'})
        assert comments_field is not None, "Comments field not found"
        assert comments_field['value'] == transaction.comments, "Comments field is not the same than transaction"

        # Check category field
        category_field = form.find('select', {'name': 'category_id'})
        assert category_field is not None, "Category field not found"
        selected_option = category_field.find('option', {'selected': True})
        if transaction.category is None:
            assert selected_option['value'] == 'None', "Selected category should be none"
        else:
            assert selected_option['value'] == str(CategoryRepository().get_by_id(
                transaction.category.id).id), "Category field is not the same than transaction"
